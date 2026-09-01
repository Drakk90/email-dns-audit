#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
 EMAIL DNS AUDIT NEON — Internationalization (i18n) Module
 Supported Languages: Spanish ('es') | English ('en')
═══════════════════════════════════════════════════════════════════════════════
"""
from typing import Callable, Optional, Dict, Any

MESSAGES: Dict[str, Dict[str, str]] = {
    "es": {
        # --- CLI & Banner ---
        "app_title": "EMAIL DNS AUDIT NEON v3.3",
        "app_subtitle": "Auditoría DNS / Autenticación de Correo",
        "author": "Eduardo Recinos",
        "ciso": "VCISO",
        "cli_desc": "Auditoría DNS y Autenticación de Correo (SPF, DMARC, DKIM, DNSSEC, MTA-STS, TLS-RPT, BIMI, RDAP).",
        "cli_domains_help": "Archivo con lista de dominios (uno por línea).",
        "cli_domain_help": "Auditar un único dominio específico.",
        "cli_outdir_help": "Carpeta donde se guardarán los resultados.",
        "cli_lang_help": "Idioma de salida y del reporte: 'es' (Español) o 'en' (Inglés).",
        "cli_concurrency_help": "Número de consultas concurrentes.",
        "cli_deep_dkim_help": "Búsqueda exhaustiva de selectores DKIM (fijos + rotativos por fecha).",
        "cli_deep_months_help": "Meses hacia atrás para selectores rotativos DKIM (default: 30).",
        "cli_selectors_help": "Selectores DKIM adicionales separados por coma.",
        "cli_dnssec_resolvers_help": "IPs de resolvers DNSSEC separadas por coma.",
        "cli_resolvers_help": "IPs de resolvers DNS separadas por coma.",
        
        # --- Estados y Severidades ---
        "status_compliant": "Cumple",
        "status_partial": "Cumple parcialmente",
        "status_non_compliant": "No cumple",
        "status_pending": "Pendiente",
        "status_not_applicable": "No aplica",
        "status_to_validate": "Por validar",
        "status_no_record": "Sin registro",
        
        "sev_critical": "Crítica",
        "sev_high": "Alta",
        "sev_medium": "Media",
        "sev_low": "Baja",
        "sev_info": "Informativa",

        "yes": "Si",
        "no": "No",
        "partial": "Parcial",
        "not_published": "No publicado",
        "no_mx": "Sin MX",
        "production": "Producción",
        "manual_validation": "Validar manualmente",
        "default_internal_owner": "Seguridad / TI",
        "privacy_protected": "Privacidad / Redactado",

        # --- Cumplimiento Global ---
        "compliance_high": "Alto ({pct}%)",
        "compliance_medium": "Medio ({pct}%)",
        "compliance_low": "Bajo ({pct}%)",

        # --- Terminal Progress & Logs ---
        "loading_domains": "Cargando lista de dominios...",
        "domains_found": "Se encontraron [bold cyan]{count}[/] dominios a auditar.",
        "starting_audit": "Iniciando auditoría en paralelo ({concurrency} workers)...",
        "audit_completed": "Auditoría finalizada.",
        "generating_excel": "Generando reporte unificado de Excel...",
        "excel_saved": "Reporte Excel guardado en: [bold green]{path}[/]",
        "evidence_saved": "Evidencias guardadas en: [bold green]{path}[/]",
        "summary_title": "RESUMEN EJECUTIVO DE AUDITORÍA",
        "col_domain": "Dominio",
        "col_spf": "SPF",
        "col_dkim": "DKIM",
        "col_dmarc": "DMARC",
        "col_dnssec": "DNSSEC",
        "col_mtasts": "MTA-STS",
        "col_tlsrpt": "TLS-RPT",
        "col_bimi": "BIMI",
        "col_compliance": "Cumplimiento",
        "col_findings": "Hallazgos",

        # --- Propósito y Mecanismo ---
        "purpose_internal": "Interno (correo corporativo)",
        "purpose_marketing": "Marketing",
        "purpose_transactional": "Transaccional",
        "mechanism_m365": "Conector M365",
        "mechanism_google": "Conector Google",
        "mechanism_smtp": "SMTP / Webmail",
        "mechanism_api_relay": "API / SMTP relay",
        "mechanism_saas": "Plataforma SaaS",

        # --- Hallazgos y Acciones Recomendadas ---
        "rec_consolidate": "Consolidar",
        "rec_reduce": "Reducir",
        "rec_change_all": "Cambiar a -all",
        "rec_harden": "Endurecer",
        "rec_publish": "Publicar",
        "rec_rotate": "Rotar",
        "rec_migrate_2048": "Migrar 2048",
        "rec_migrate_quarantine": "Migrar quarantine",
        "rec_migrate_reject": "Migrar reject",
        "rec_check_ds": "Revisar DS",
        "rec_publish_ds": "Publicar DS",
        "rec_activate": "Activar",
        "rec_acquire_vmc": "Adquirir",
        "rec_get_selector": "Obtener selector real de un correo enviado y reauditar con --selectors",
        "rec_retry_deep": "Reintentar con --deep-dkim o pasar el selector real con --selectors",

        "f_spf_multi": "Múltiples registros SPF",
        "f_spf_lookups": ">10 lookups DNS",
        "f_spf_plus_all": "Directiva +all insegura",
        "f_spf_soft": "Directiva {val} débil",
        "f_spf_none": "Sin registro SPF publicado",
        "f_dkim_bits_low": "Clave DKIM <1024 bits ({selector})",
        "f_dkim_bits_med": "Clave DKIM <2048 bits ({selector})",
        "f_dkim_not_found_deep": "No detectado ni en búsqueda profunda (selector custom)",
        "f_dkim_not_found_common": "No detectado entre selectores comunes (puede usar selector custom)",
        "f_dmarc_none": "Sin registro DMARC publicado",
        "f_dmarc_p_none": "Política DMARC p=none (sólo monitoreo)",
        "f_dmarc_p_quar": "Política DMARC p=quarantine",
        "f_dnssec_bogus": "Cadena DNSSEC rota (Bogus)",
        "f_dnssec_incomplete": "Sin registro DS en el registrador",
        "f_dnssec_none": "Sin DNSSEC implementado",
        "f_mtasts_none": "MTA-STS no implementado",
        "f_tlsrpt_none": "TLS-RPT no implementado",
        "f_bimi_no_vmc": "BIMI publicado sin certificado VMC",

        # --- Excel Sheets & Headers ---
        "sheet_summary": "Resumen",
        "sheet_inventory": "Inventario_Dominios",
        "sheet_spf": "SPF",
        "sheet_dmarc": "DMARC",
        "sheet_dkim": "DKIM",
        "sheet_dnssec": "DNSSEC",
        "sheet_mtasts": "Complementos",
        "sheet_bimi": "BIMI",
        "sheet_senders": "Remitentes_Autorizados",
        "sheet_findings": "Hallazgos",
        "sheet_glossary": "Glosario",

        "card_total_domains": "DOMINIOS TOTALES",
        "card_critical_findings": "HALLAZGOS CRÍTICOS",
        "card_high_findings": "HALLAZGOS ALTOS",
        "card_avg_compliance": "CUMPLIMIENTO PROMEDIO",
        "card_dmarc_reject": "DMARC REJECT",
        "card_dnssec_secure": "DNSSEC SEGURO",
    },

    "en": {
        # --- CLI & Banner ---
        "app_title": "EMAIL DNS AUDIT NEON v3.3",
        "app_subtitle": "DNS Audit / Email Authentication",
        "author": "Eduardo Recinos",
        "ciso": "VCISO",
        "cli_desc": "DNS Audit and Email Authentication (SPF, DMARC, DKIM, DNSSEC, MTA-STS, TLS-RPT, BIMI, RDAP).",
        "cli_domains_help": "File containing domain list (one per line).",
        "cli_domain_help": "Audit a single specific domain.",
        "cli_outdir_help": "Output folder where results will be saved.",
        "cli_lang_help": "Output and report language: 'es' (Spanish) or 'en' (English).",
        "cli_concurrency_help": "Number of concurrent queries.",
        "cli_deep_dkim_help": "Exhaustive DKIM selector discovery (common + date-rotated).",
        "cli_deep_months_help": "Months back for date-rotated DKIM selectors (default: 30).",
        "cli_selectors_help": "Additional comma-separated DKIM selectors.",
        "cli_dnssec_resolvers_help": "Comma-separated DNSSEC resolver IPs.",
        "cli_resolvers_help": "Comma-separated DNS resolver IPs.",

        # --- States & Severities ---
        "status_compliant": "Compliant",
        "status_partial": "Partially compliant",
        "status_non_compliant": "Non-compliant",
        "status_pending": "Pending",
        "status_not_applicable": "Not applicable",
        "status_to_validate": "To validate",
        "status_no_record": "No record",

        "sev_critical": "Critical",
        "sev_high": "High",
        "sev_medium": "Medium",
        "sev_low": "Low",
        "sev_info": "Informational",

        "yes": "Yes",
        "no": "No",
        "partial": "Partial",
        "not_published": "Not published",
        "no_mx": "No MX",
        "production": "Production",
        "manual_validation": "Validate manually",
        "default_internal_owner": "Security / IT",
        "privacy_protected": "Privacy / Redacted",

        # --- Global Compliance ---
        "compliance_high": "High ({pct}%)",
        "compliance_medium": "Medium ({pct}%)",
        "compliance_low": "Low ({pct}%)",

        # --- Terminal Progress & Logs ---
        "loading_domains": "Loading domain list...",
        "domains_found": "Found [bold cyan]{count}[/] domains to audit.",
        "starting_audit": "Starting parallel audit ({concurrency} workers)...",
        "audit_completed": "Audit completed.",
        "generating_excel": "Generating unified Excel report...",
        "excel_saved": "Excel report saved to: [bold green]{path}[/]",
        "evidence_saved": "Evidence logs saved to: [bold green]{path}[/]",
        "summary_title": "AUDIT EXECUTIVE SUMMARY",
        "col_domain": "Domain",
        "col_spf": "SPF",
        "col_dkim": "DKIM",
        "col_dmarc": "DMARC",
        "col_dnssec": "DNSSEC",
        "col_mtasts": "MTA-STS",
        "col_tlsrpt": "TLS-RPT",
        "col_bimi": "BIMI",
        "col_compliance": "Compliance",
        "col_findings": "Findings",

        # --- Purpose & Mechanism ---
        "purpose_internal": "Internal (corporate email)",
        "purpose_marketing": "Marketing",
        "purpose_transactional": "Transactional",
        "mechanism_m365": "M365 Connector",
        "mechanism_google": "Google Connector",
        "mechanism_smtp": "SMTP / Webmail",
        "mechanism_api_relay": "API / SMTP relay",
        "mechanism_saas": "SaaS Platform",

        # --- Findings & Recommended Actions ---
        "rec_consolidate": "Consolidate",
        "rec_reduce": "Reduce",
        "rec_change_all": "Change to -all",
        "rec_harden": "Harden",
        "rec_publish": "Publish",
        "rec_rotate": "Rotate",
        "rec_migrate_2048": "Migrate to 2048",
        "rec_migrate_quarantine": "Migrate to quarantine",
        "rec_migrate_reject": "Migrate to reject",
        "rec_check_ds": "Review DS",
        "rec_publish_ds": "Publish DS",
        "rec_activate": "Activate",
        "rec_acquire_vmc": "Acquire",
        "rec_get_selector": "Obtain real selector from sent email header and re-run with --selectors",
        "rec_retry_deep": "Retry with --deep-dkim or pass real selector with --selectors",

        "f_spf_multi": "Multiple SPF records",
        "f_spf_lookups": ">10 DNS lookups",
        "f_spf_plus_all": "Insecure +all directive",
        "f_spf_soft": "Weak {val} directive",
        "f_spf_none": "No SPF record published",
        "f_dkim_bits_low": "DKIM key <1024 bits ({selector})",
        "f_dkim_bits_med": "DKIM key <2048 bits ({selector})",
        "f_dkim_not_found_deep": "Not detected even in deep search (custom selector)",
        "f_dkim_not_found_common": "Not detected among common selectors (may use custom selector)",
        "f_dmarc_none": "No DMARC record published",
        "f_dmarc_p_none": "DMARC policy p=none (monitoring only)",
        "f_dmarc_p_quar": "DMARC policy p=quarantine",
        "f_dnssec_bogus": "Broken DNSSEC chain (Bogus)",
        "f_dnssec_incomplete": "Missing DS record at registrar",
        "f_dnssec_none": "DNSSEC not implemented",
        "f_mtasts_none": "MTA-STS not implemented",
        "f_tlsrpt_none": "TLS-RPT not implemented",
        "f_bimi_no_vmc": "BIMI published without VMC certificate",

        # --- Excel Sheets & Headers ---
        "sheet_summary": "Summary",
        "sheet_inventory": "Domain_Inventory",
        "sheet_spf": "SPF",
        "sheet_dmarc": "DMARC",
        "sheet_dkim": "DKIM",
        "sheet_dnssec": "DNSSEC",
        "sheet_mtasts": "Addons",
        "sheet_bimi": "BIMI",
        "sheet_senders": "Authorized_Senders",
        "sheet_findings": "Findings",
        "sheet_glossary": "Glossary",

        "card_total_domains": "TOTAL DOMAINS",
        "card_critical_findings": "CRITICAL FINDINGS",
        "card_high_findings": "HIGH FINDINGS",
        "card_avg_compliance": "AVERAGE COMPLIANCE",
        "card_dmarc_reject": "DMARC REJECT",
        "card_dnssec_secure": "DNSSEC SECURE",
    }
}


def get_translator(lang: str = "es") -> Callable[..., str]:
    """Returns a translation function for the given language ('es' or 'en')."""
    active_lang = "en" if str(lang).lower().startswith("en") else "es"

    def translate(key: str, default: Optional[str] = None, **kwargs: Any) -> str:
        lang_dict = MESSAGES.get(active_lang, MESSAGES["es"])
        msg = lang_dict.get(key, MESSAGES["es"].get(key, default or key))
        if kwargs:
            try:
                return msg.format(**kwargs)
            except Exception:
                return msg
        return msg

    return translate
