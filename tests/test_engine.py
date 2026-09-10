import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import kb_loader, engine, scoring, web_lookup, fallback

RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class TestKBLoader(unittest.TestCase):
    def test_loads_all_rule_files_without_error(self):
        rules = kb_loader.load_rules(RULES_DIR)
        self.assertGreater(len(rules), 0)
        regs = {r["regulation"] for r in rules}
        self.assertIn("GDPR", regs)
        self.assertIn("WCAG", regs)
        self.assertIn("PCI-DSS", regs)
        self.assertIn("LGPD", regs)
        self.assertIn("COPPA", regs)
        self.assertIn("PIPEDA", regs)

    def test_official_sources_registry_not_picked_up_as_pattern_rules(self):
        # official_sources.yaml has no "rules:" list with the required
        # fields, so kb_loader should either skip it gracefully or the file
        # naming convention keeps it separate. Confirm it doesn't crash the
        # loader and doesn't produce a bogus "regulation" of its own.
        rules = kb_loader.load_rules(RULES_DIR)
        regs = {r["regulation"] for r in rules}
        self.assertNotIn("UNKNOWN", regs)


class TestScoring(unittest.TestCase):
    def test_risk_score_bounds(self):
        s = scoring.risk_score(5, 5, 1.3)
        self.assertLessEqual(s, 100.0)
        s2 = scoring.risk_score(1, 1, 0.7)
        self.assertGreater(s2, 0)

    def test_confidence_halved_by_negative_pattern(self):
        c1 = scoring.confidence(0.8, negative_pattern_hit=False)
        c2 = scoring.confidence(0.8, negative_pattern_hit=True)
        self.assertAlmostEqual(c2, c1 / 2, places=2)

    def test_category_readiness_full_when_no_findings(self):
        self.assertEqual(scoring.category_readiness([]), 100.0)


class TestWebLookup(unittest.TestCase):
    def test_finds_registry_entry_for_known_regulation(self):
        entry = web_lookup.find_registry_entry("GDPR")
        self.assertIsNotNone(entry)
        self.assertIn("eur-lex.europa.eu", entry["official_domains"])

    def test_finds_registry_entry_by_partial_name(self):
        entry = web_lookup.find_registry_entry("LGPD")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["code"], "LGPD")

    def test_official_gov_domain_allowed_via_registry(self):
        entry = web_lookup.find_registry_entry("GDPR")
        result = web_lookup.is_allowed_domain("https://eur-lex.europa.eu/some-page", entry)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["tier"], "registry")

    def test_third_party_blog_blocked_even_if_relevant(self):
        entry = web_lookup.find_registry_entry("GDPR")
        result = web_lookup.is_allowed_domain("https://some-compliance-blog.com/gdpr-guide", entry)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["tier"], "blocked")

    def test_unknown_dot_gov_domain_allowed_heuristically(self):
        result = web_lookup.is_allowed_domain("https://example.gov/notice", None)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["tier"], "heuristic")

    def test_medium_blog_always_blocked(self):
        result = web_lookup.is_allowed_domain("https://medium.com/@someone/gdpr-explained", None)
        self.assertFalse(result["allowed"])

    def test_lookup_instructions_known_regulation_names_official_domains_only(self):
        result = web_lookup.lookup_instructions("CCPA")
        self.assertEqual(result["status"], "in_registry")
        self.assertIn("cppa.ca.gov", result["official_domains"])

    def test_lookup_instructions_unknown_regulation_forces_gov_domain_check(self):
        result = web_lookup.lookup_instructions("Thailand PDPA")
        self.assertEqual(result["status"], "not_in_registry")
        self.assertIn("REJECT", result["instructions"])


class TestFallback(unittest.TestCase):
    def test_build_lookup_request_for_registry_regulation(self):
        result = fallback.build_lookup_request("HIPAA")
        self.assertEqual(result["status"], "in_registry")

    def test_check_source_rejects_non_official_url(self):
        result = fallback.check_source("https://acme-compliance-blog.com/hipaa", "HIPAA")
        self.assertFalse(result["allowed"])


class TestEngineOnFixtures(unittest.TestCase):
    def setUp(self):
        self.rules = kb_loader.load_rules(RULES_DIR)

    def test_finds_tracking_without_consent(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("gdpr-001", ids)

    def test_finds_missing_alt_text(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("wcag-001", ids)

    def test_finds_missing_input_label(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("wcag-002", ids)

    def test_finds_non_keyboard_click_handler(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("wcag-003", ids)

    def test_finds_raw_card_number_pattern(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["Global"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("pci-001", ids)

    def test_good_tracker_has_lower_confidence_due_to_consent_check(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU"])
        good_finding = [f for f in result["findings"]
                         if f["rule_id"] == "gdpr-001" and f["file"].endswith("good_tracker.js")]
        # good_tracker.js has hasConsent nearby -> negative pattern hit -> lower confidence
        if good_finding:
            self.assertTrue(good_finding[0]["mitigation_signal_found"])

    def test_finds_lgpd_tracking_without_consent(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["BR"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("lgpd-001", ids)

    def test_finds_lgpd_missing_rights_endpoint(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["BR"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("lgpd-002", ids)

    def test_finds_coppa_age_field_without_parental_consent(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["US"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("coppa-001", ids)

    def test_finds_pipeda_missing_purpose_statement(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["CA"])
        ids = {f["rule_id"] for f in result["findings"]}
        self.assertIn("pipeda-001", ids)

    def test_scan_repo_raises_on_nonexistent_path(self):
        # A bad/mistyped path must error, not silently return a fake
        # 100/100-readiness "clean" scan (that would be indistinguishable
        # from an actually clean scan and is actively misleading).
        with self.assertRaises(FileNotFoundError):
            engine.scan_repo("/definitely/does/not/exist/xyz123", self.rules, ["EU"])

    def test_readiness_scores_present_for_all_categories(self):
        result = engine.scan_repo(FIXTURES_DIR, self.rules, ["EU", "US-CA", "US"])
        self.assertIn("GDPR", result["category_readiness"])
        self.assertIn("WCAG", result["category_readiness"])
        self.assertLessEqual(result["overall_readiness"], 100.0)


if __name__ == "__main__":
    unittest.main()
