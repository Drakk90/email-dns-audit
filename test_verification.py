import unittest
import openpyxl
from email_dns_audit_neon import evaluate_ciso_compliance_and_score, build_excel
from i18n import get_translator
from pathlib import Path
import tempfile

class TestVerification(unittest.TestCase):
    def test_weighted_compliance_and_aggregation(self):
        t_es = get_translator("es")
        # Dummy domain data
        info = {
            "domain": "test.com",
            "spf": {"pub": "si", "all": "-all", "multi": "no", "lookups": 2},
            "dmarc": {"pub": "si", "p": "reject", "pct": "100"},
            "dnssec": {"diag": "Secure"},
            "mtasts": {"mode": "enforce"},
            "tlsrpt": {"pub": "si"},
            "bimi": {"pub": "si"},
            "dkim": [{"selector": "s1", "bits": 2048, "service": "Test"}]
        }
        score, grade, matrix = evaluate_ciso_compliance_and_score(info, [], [], t=t_es)
        self.assertGreaterEqual(score, 85)
        self.assertEqual(grade, "A")

    def test_dynamic_formulas_spanish(self):
        t_es = get_translator("es")
        with tempfile.TemporaryDirectory() as tmpdir:
            outdir = Path(tmpdir)
            data = {
                "inventario": [[1, "test.com", "Prod", "Test", "Reg", "2028-01-01", "Si", "Sec", "NS", "si", "cas", "OK", "Score: 90 (A)"]],
                "resumen": [["test.com", "Reg", "2020", "2028", "ok", "Signed", "ns", "123", "Secure", "si", "-all", 2, 0, "no", "si", "reject", None, "100", "rua", "MX", "enforce", "si", "si", 0.90]],
                "spf": [], "dkim": [], "dmarc": [], "dnssec": [], "mtasts": [], "tlsrpt": [], "bimi": [], "remit": [], "easm": [], "compliance": [], "caa_tls": []
            }
            hallazgos = [["H-001", "test.com", "SPF", "Desc", "Crítica", "Action"]]
            stats = {"total_domains": 1, "sev_count": {"Crítica": 1}, "ciso_score": "90 (A)", "avg_compliance": 90.0}
            xlsx_path = build_excel(outdir, data, hallazgos, stats, None, t=t_es)
            wb = openpyxl.load_workbook(xlsx_path, data_only=False)
            ws_resumen = wb["Resumen"]
            self.assertEqual(ws_resumen["A5"].value, "=COUNTA('Inventario_Dominios'!B2:B2)")
            self.assertEqual(ws_resumen["D5"].value, '=COUNTIF(\'Hallazgos\'!E2:E2, "Crítica")')
            self.assertEqual(ws_resumen["M5"].value, "=AVERAGE('Resumen_Consolidado'!X2:X2)")
            self.assertEqual(ws_resumen["M5"].number_format, "0.0%")
            ws_cons = wb["Resumen_Consolidado"]
            self.assertEqual(ws_cons["X2"].number_format, "0.0%")
            self.assertEqual(ws_cons["X2"].value, 0.90)

    def test_dynamic_formulas_english(self):
        t_en = get_translator("en")
        with tempfile.TemporaryDirectory() as tmpdir:
            outdir = Path(tmpdir)
            data = {
                "inventario": [[1, "test.com", "Prod", "Test", "Reg", "2028-01-01", "Yes", "Sec", "NS", "yes", "cas", "OK", "Score: 90 (A)"]],
                "resumen": [["test.com", "Reg", "2020", "2028", "ok", "Signed", "ns", "123", "Secure", "yes", "-all", 2, 0, "no", "yes", "reject", None, "100", "rua", "MX", "enforce", "yes", "yes", 0.90]],
                "spf": [], "dkim": [], "dmarc": [], "dnssec": [], "mtasts": [], "tlsrpt": [], "bimi": [], "remit": [], "easm": [], "compliance": [], "caa_tls": []
            }
            hallazgos = [["H-001", "test.com", "SPF", "Desc", "Critical", "Action"]]
            stats = {"total_domains": 1, "sev_count": {"Critical": 1}, "ciso_score": "90 (A)", "avg_compliance": 90.0}
            xlsx_path = build_excel(outdir, data, hallazgos, stats, None, t=t_en)
            wb = openpyxl.load_workbook(xlsx_path, data_only=False)
            ws_summary = wb["Summary"]
            self.assertEqual(ws_summary["A5"].value, "=COUNTA('Domain_Inventory'!B2:B2)")
            self.assertEqual(ws_summary["D5"].value, '=COUNTIF(\'Findings\'!E2:E2, "Critical")')
            self.assertEqual(ws_summary["M5"].value, "=AVERAGE('Consolidated_Summary'!X2:X2)")
            self.assertEqual(ws_summary["M5"].number_format, "0.0%")
            ws_cons = wb["Consolidated_Summary"]
            self.assertEqual(ws_cons["X2"].number_format, "0.0%")
            self.assertEqual(ws_cons["X2"].value, 0.90)

if __name__ == "__main__":
    unittest.main()
