#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
 EMAIL DNS AUDIT NEON v3.2 — Excel Unificado
 Auditoria DNS / Email Authentication
───────────────────────────────────────────────────────────────────────────────
 Autor   : Eduardo Recinos
 CISO    : VCISO
 Version : 3.2
 Fecha   : 2026-06-30
 Cambios v3.2:
   - DKIM: lista balanceada (~50 selectores comunes) por defecto.
   - Nuevo flag --deep-dkim: busqueda exhaustiva con selectores rotativos
     por fecha (Google, Microsoft, Amazon SES, SparkPost, etc.).
   - DKIM: mensaje diferenciado "Sin DKIM" vs "No detectado (selector no comun)".
   - Se mantiene DNSSEC multi-resolver interno (una sola carpeta de salida).
═══════════════════════════════════════════════════════════════════════════════
"""
import sys, os, re, time, base64, argparse, asyncio, subprocess, importlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

REQUIRED = {
    "rich": "rich>=13.7.0", "dns": "dnspython>=2.4.0",
    "cryptography": "cryptography>=42.0.0", "httpx": "httpx>=0.27.0",
    "whois": "python-whois>=0.9.0", "aiodns": "aiodns>=3.1.0",
    "openpyxl": "openpyxl>=3.1.0",
}


def check_deps(auto=False):
    missing = []
    for mod, pip_name in REQUIRED.items():
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(pip_name)
    if not missing:
        return True
    msg = ("\n\033[91m[!] Faltan dependencias:\033[0m\n  " + "\n  ".join(missing) +
           "\n\n\033[96mInstalar:\033[0m\n  pip install --user " + " ".join(missing) +
           "\n\n\033[96mO ejecuta:\033[0m\n  python3 " + sys.argv[0] + " --install-deps\n")
    if auto:
        print("\033[93m[*] Instalando dependencias...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", *missing])
        print("\033[92m[OK] Re-ejecuta el script.\033[0m")
        sys.exit(0)
    print(msg)
    return False


if "--install-deps" in sys.argv:
    check_deps(auto=True)
if not check_deps():
    sys.exit(1)

import dns.resolver, dns.asyncresolver, dns.flags, dns.rcode
import dns.message, dns.asyncquery
import httpx
import whois as whois_lib
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.box import DOUBLE, ROUNDED, HEAVY
from rich.style import Style
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

# Paleta corporativa
C_DARK = "0E3178"; C_NAVY = "0D1C43"; C_MID = "004E96"; C_BLUE = "0066B3"
C_ACC = "2B96CD"; C_SOFT = "8FC2E0"; C_BAND = "EAF3FA"; C_WHITE = "FFFFFF"

# Paleta neon consola
NM = "#ff00ff"; NC = "#00ffff"; NG = "#39ff14"; NO = "#ff6600"
NR = "#ff003c"; NY = "#ffff00"; NP = "#9d00ff"

# =============================================================================
#  OPCION A — Lista balanceada de selectores DKIM comunes (~50)
#  Cubre las plataformas mas usadas sin inflar demasiado las consultas.
# =============================================================================
COMMON_SELECTORS = [
    # Microsoft 365 / Outlook
    "selector1", "selector2",
    # Google Workspace
    "google",
    # SendGrid
    "s1", "s2", "smtpapi", "em",
    # Mailchimp / Mandrill
    "k1", "k2", "k3", "mandrill", "mte1", "mte2",
    # Mailgun
    "mx", "mg", "smtp", "pic", "mailo",
    # Amazon SES
    "ses", "amazonses", "ses-1", "ses-2",
    # Postmark
    "pm", "20150623", "20150625",
    # SparkPost
    "scph0817", "scph0816", "sparkpostmail", "sp",
    # Zoho
    "zoho", "zmail",
    # HubSpot
    "hubspotemail1", "hubspotemail2", "hs1", "hs2",
    # Proofpoint / Mimecast
    "ppdkim", "mimecast",
    # Salesforce / Marketing Cloud
    "et", "200608",
    # Klaviyo / Constant Contact / Zendesk / Freshdesk
    "kl", "kl2", "roving", "zendesk1", "zendesk2", "fd", "fd2",
    # MXVault / Dyn / Everlytic / Proton
    "mxvault", "dynect", "everlytickey1", "everlytickey2", "sm", "proton",
    # Genericos
    "dkim", "mail", "default",
]

console = Console()


# =============================================================================
#  DEEP DKIM — Generacion exhaustiva de selectores (activado con --deep-dkim)
#  Incluye selectores rotativos por fecha de grandes proveedores.
# =============================================================================
def generate_deep_selectors(months_back=30):
    """Genera una lista ampliada de selectores para busqueda profunda.
    Incluye:
      - Selectores fijos adicionales de grandes plataformas.
      - Selectores rotativos por fecha (patron YYYYMMDD y YYYYMM) usados por
        Google, Amazon SES, Postmark, SparkPost y otros, para los ultimos
        'months_back' meses (dia 1 de cada mes)."""
    deep = set()

    # --- Selectores fijos adicionales de grandes proveedores ---
    deep.update([
        # Google (ademas de rotativos por fecha)
        "google2", "goog", "gmail",
        # Microsoft (dominios onmicrosoft y variantes)
        "selector1-onmicrosoft-com", "selector2-onmicrosoft-com", "s1024", "s2048",
        # Amazon SES (selectores con prefijo)
        "amazonses1", "amazonses2", "aws", "awsses",
        # SendGrid rotativos
        "s3", "s4", "sendgrid", "sg", "sig1",
        # Mailgun rotativos
        "mailgun", "mg1", "mg2", "k2mg", "email",
        # SparkPost rotativos historicos
        "scph0316", "scph0517", "scph0916", "scph1016", "scph1216",
        "scph0118", "scph0218", "scph0318", "scph0618", "scph1017",
        # Postmark rotativos historicos
        "20161025", "20170101", "20180101", "20190101", "20200101",
        # Zendesk / Freshdesk / Klaviyo extendidos
        "zendesk", "freshdesk", "klaviyo", "kl3",
        # HubSpot rotativos
        "hs3", "hs4", "hubspot",
        # Marketing Cloud / Salesforce
        "mc", "sfmc", "exacttarget", "cust", "mta",
        # Otros proveedores grandes
        "cm", "createsend", "campaignmonitor",   # Campaign Monitor
        "litmus", "sailthru", "sailthru1",        # Sailthru
        "mktomail", "m1", "marketo",              # Marketo
        "pardot", "psdkim",                       # Pardot
        "sib", "sendinblue", "brevo",             # Brevo / Sendinblue
        "cc", "ctct",                             # Constant Contact
        "intercom", "ic",                         # Intercom
        "mailerlite", "ml",                       # MailerLite
        "omnisend", "os",                         # Omnisend
        "activecampaign", "ac",                   # ActiveCampaign
        "drip", "dr",                             # Drip
        "twilio", "tw",                           # Twilio
        "mailjet1", "mailjet2",                   # Mailjet
        "elasticemail", "ee",                     # Elastic Email
        "smtp2go", "s2g",                         # SMTP2GO
        "socketlabs", "sl",                       # SocketLabs
        "turbosmtp", "ts",                        # TurboSMTP
        "mailpoet", "mp",                         # MailPoet
        "protonmail", "protonmail2", "protonmail3",  # Proton rotativos
        "fm1", "fm2", "fm3",                      # Fastmail
        "dkim1", "dkim2", "key1", "key2",         # Genericos numerados
    ])

    # --- Selectores rotativos por fecha ---
    # Google y otros rotan con patron YYYYMMDD (dia 1) y algunos YYYYMM.
    today = datetime.now(timezone.utc)
    for i in range(months_back + 1):
        # Retroceder i meses de forma aproximada (dia 1)
        y = today.year
        mth = today.month - i
        while mth <= 0:
            mth += 12
            y -= 1
        deep.add(f"{y:04d}{mth:02d}01")   # YYYYMMDD (dia 1)
        deep.add(f"{y:04d}{mth:02d}")     # YYYYMM
        # Google historicamente ha usado tambien dia 15
        deep.add(f"{y:04d}{mth:02d}15")

    return sorted(deep)


def map_dkim_service(s):
    m = {"selector1": "Microsoft 365", "selector2": "Microsoft 365", "google": "Google Workspace",
         "k1": "Mailchimp / SendGrid", "k2": "Mailchimp / SendGrid", "k3": "Mailchimp / SendGrid",
         "smtpapi": "SendGrid", "mandrill": "Mandrill (Mailchimp transaccional)",
         "fd": "Mailgun", "fd2": "Mailgun", "pic": "Postmark", "pm": "Postmark", "mxvault": "MXVault",
         "ses-1": "Amazon SES", "ses-2": "Amazon SES", "ses": "Amazon SES", "amazonses": "Amazon SES",
         "zoho": "Zoho Mail", "zmail": "Zoho Mail", "dynect": "Dyn",
         "hubspotemail1": "HubSpot", "hubspotemail2": "HubSpot", "hs1": "HubSpot", "hs2": "HubSpot",
         "everlytickey1": "Everlytic", "everlytickey2": "Everlytic", "sm": "SparkPost",
         "scph0817": "SparkPost", "scph0816": "SparkPost", "sparkpostmail": "SparkPost", "sp": "SparkPost",
         "proton": "Proton Mail", "mx": "Mailgun", "mg": "Mailgun", "smtp": "Mailgun",
         "em": "SendGrid", "s1": "SendGrid / Generico", "s2": "SendGrid / Generico",
         "ppdkim": "Proofpoint", "mimecast": "Mimecast", "et": "Salesforce Marketing Cloud",
         "roving": "Constant Contact", "zendesk1": "Zendesk", "zendesk2": "Zendesk",
         "kl": "Klaviyo", "kl2": "Klaviyo", "mte1": "Mandrill", "mte2": "Mandrill",
         "dkim": "Generico / Por validar", "mail": "Generico / Por validar",
         "default": "Generico / Por validar"}
    if s in m:
        return m[s]
    # Heuristicas para selectores rotativos por fecha o prefijos conocidos
    if re.fullmatch(r"20\d{4,6}", s):
        return "Google / Rotativo por fecha"
    if s.startswith("scph"):
        return "SparkPost"
    if s.startswith("hs"):
        return "HubSpot"
    if s.startswith("ses") or s.startswith("amazonses"):
        return "Amazon SES"
    if s.startswith("mg") or s.startswith("mailgun"):
        return "Mailgun"
    if s.startswith("protonmail"):
        return "Proton Mail"
    return "Por validar (selector custom)"


def map_provider_purpose(p):
    if p in ("Microsoft 365", "Google Workspace", "Zoho Mail", "Proton Mail"):
        return "Interno (correo corporativo)"
    if p in ("Mailchimp", "HubSpot", "Mailjet", "Everlytic"):
        return "Marketing"
    if p in ("SendGrid", "Mailgun", "Amazon SES", "Postmark", "SparkPost", "Mandrill",
             "Mandrill (Mailchimp transaccional)", "Mailchimp / SendGrid"):
        return "Transaccional"
    return "Por validar"


def map_provider_mechanism(p):
    if p == "Microsoft 365":
        return "Conector M365"
    if p == "Google Workspace":
        return "Conector Google"
    if p in ("Zoho Mail", "Proton Mail"):
        return "SMTP / Webmail"
    if p in ("SendGrid", "Mailgun", "Amazon SES", "Postmark", "SparkPost", "Mandrill",
             "Mandrill (Mailchimp transaccional)", "Mailjet", "Mailchimp / SendGrid"):
        return "API / SMTP relay"
    if p in ("Mailchimp", "HubSpot", "Everlytic"):
        return "Plataforma SaaS"
    return "Por validar"


def derive_spf_status(pub, a, lk, v, m):
    if pub == "no": return "No cumple"
    if m == "si": return "No cumple"
    if a == "+all": return "No cumple"
    if lk > 10: return "No cumple"
    if v > 2: return "No cumple"
    if a in ("?all", "sin all"): return "Cumple parcialmente"
    if v >= 1: return "Cumple parcialmente"
    if lk >= 8: return "Cumple parcialmente"
    return "Cumple"


def derive_spf_severity(pub, a, lk, v, m):
    if m == "si": return "Critica"
    if a == "+all": return "Critica"
    if pub == "no": return "Alta"
    if lk > 10: return "Alta"
    if a in ("?all", "sin all"): return "Alta"
    if v > 2: return "Media"
    if v >= 1: return "Baja"
    if lk >= 8: return "Baja"
    return "Informativa"


def derive_dmarc_status(pub, p, sp, pct, rua):
    if pub == "no": return "No cumple"
    if p == "none": return "No cumple"
    if p == "reject" and pct == "100" and rua and sp: return "Cumple"
    return "Cumple parcialmente"


def derive_dmarc_severity(pub, p, sp, pct, rua):
    if pub == "no": return "Critica"
    if p == "none" or not rua: return "Alta"
    if p == "quarantine" or pct != "100": return "Media"
    if p == "reject" and not sp: return "Baja"
    return "Informativa"


def derive_dnssec_status(d):
    if d == "Secure": return "Cumple"
    if d.startswith("Firmado"): return "Cumple"
    if d.startswith("Incompleto"): return "Cumple parcialmente"
    if d == "No implementado" or d.startswith("Bogus"): return "No cumple"
    return "Pendiente"


def derive_dnssec_severity(d):
    if d.startswith("Bogus"): return "Critica"
    if d.startswith("Incompleto"): return "Alta"
    if d == "No implementado": return "Media"
    if d == "Secure": return "Informativa"
    if d.startswith("Firmado"): return "Informativa"
    return "Media"


def derive_dkim_status(bits, t, rev):
    if rev.startswith("si"): return "No cumple"
    if isinstance(bits, int):
        if bits < 1024: return "No cumple"
        if bits < 2048: return "Cumple parcialmente"
    else:
        return "Pendiente"
    if t == "y": return "Cumple parcialmente"
    return "Cumple"


def derive_dkim_severity(bits, t, rev):
    if rev.startswith("si"): return "Critica"
    if isinstance(bits, int):
        if bits < 1024: return "Critica"
        if bits < 2048: return "Alta"
    else:
        return "Media"
    if t == "y": return "Media"
    return "Informativa"


def derive_mtasts_status(pub, mode, acc):
    if pub == "no": return "No cumple"
    if acc == "no": return "No cumple"
    if mode == "enforce": return "Cumple"
    if mode == "testing": return "Cumple parcialmente"
    if mode == "none": return "No cumple"
    return "Pendiente"


def derive_tlsrpt_status(pub, rua):
    if pub == "no": return "No cumple"
    if not rua: return "Pendiente"
    return "Cumple"


def derive_bimi_status(pub, svg, vmc):
    if pub == "no": return "No cumple"
    if not svg: return "No cumple"
    if vmc == "Si": return "Cumple"
    if vmc == "No": return "No cumple"
    return "Cumple parcialmente"


def derive_remit_state(spf, dkim, dmarc):
    y = sum(1 for v in (spf, dkim, dmarc) if v == "Si")
    n = sum(1 for v in (spf, dkim, dmarc) if v == "No")
    if y == 3: return "Cumple"
    if n == 3: return "No cumple"
    if y >= 1: return "Cumple parcialmente"
    return "Por validar"


def write_evidence(outdir, domain, filename, command, content, resolver):
    path = outdir / "evidencias" / domain / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    h = (f"# Evidencia: {filename}\n# Dominio: {domain}\n# Comando: {command}\n"
         f"# Timestamp: {datetime.now(timezone.utc).isoformat()}\n# Resolver: {resolver}\n# -----\n")
    path.write_text(h + (content or "") + "\n", encoding="utf-8")


async def q(resolver_obj, name, rdtype):
    try:
        return await resolver_obj.resolve(name, rdtype, lifetime=6)
    except Exception:
        return None


async def check_whois(domain, outdir, resolver):
    loop = asyncio.get_event_loop()
    try:
        w = await loop.run_in_executor(None, whois_lib.whois, domain)
        raw = str(w)
        reg = getattr(w, "registrar", None) or "N/D"
        cr = getattr(w, "creation_date", None)
        if isinstance(cr, list): cr = cr[0] if cr else None
        ex = getattr(w, "expiration_date", None)
        if isinstance(ex, list): ex = ex[0] if ex else None
        st = getattr(w, "status", None) or "N/D"
        if isinstance(st, list): st = ";".join(str(x) for x in st[:3])
        ds = getattr(w, "dnssec", None) or "N/D"
        write_evidence(outdir, domain, "whois.txt", f"whois {domain}", raw, resolver)
        return {"registrar": str(reg)[:200], "created": str(cr) if cr else "N/D",
                "expires": str(ex) if ex else "N/D", "status": str(st)[:200], "dnssec_whois": str(ds)}
    except Exception as e:
        write_evidence(outdir, domain, "whois.txt", f"whois {domain}", f"ERROR: {e}", resolver)
        return {"registrar": "N/D", "created": "N/D", "expires": "N/D", "status": "N/D", "dnssec_whois": "N/D"}


async def check_ns_soa(domain, ro, outdir, ip):
    ns = await q(ro, domain, "NS")
    soa = await q(ro, domain, "SOA")
    ns_list = sorted([str(r.target).rstrip(".") for r in ns]) if ns else []
    soa_serial = "N/D"
    if soa:
        try:
            soa_serial = str(soa[0].serial)
        except Exception:
            pass
    ns_str = ";".join(ns_list) if ns_list else "N/D"
    write_evidence(outdir, domain, "dig_ns.txt", f"NS {domain}", ns_str, ip)
    prov = "Otro / Personalizado"
    low = ns_str.lower()
    if "cloudflare" in low: prov = "Cloudflare"
    elif "awsdns" in low: prov = "AWS Route 53"
    elif "azure-dns" in low: prov = "Azure DNS"
    elif "googledomains" in low or "google.com" in low: prov = "Google Cloud DNS"
    elif "godaddy" in low or "domaincontrol" in low: prov = "GoDaddy"
    elif "namecheap" in low: prov = "Namecheap"
    return {"ns_list": ns_str, "soa_serial": soa_serial, "ns_provider": prov}


async def _probe_ad_bit(domain, resolver_ip):
    """Prueba el bit AD contra un resolver validador especifico.
    Devuelve (ad, status, dump). ad = 'si'/'no', status = rcode."""
    ad = "no"; status = "N/D"; dump = ""
    try:
        query = dns.message.make_query(domain, "A", want_dnssec=True)
        query.flags |= dns.flags.AD
        try:
            response = await dns.asyncquery.udp(query, resolver_ip, timeout=6)
            if response.flags & dns.flags.TC:  # truncada -> reintentar TCP
                response = await dns.asyncquery.tcp(query, resolver_ip, timeout=6)
        except Exception:
            response = await dns.asyncquery.tcp(query, resolver_ip, timeout=6)
        status = dns.rcode.to_text(response.rcode())
        if response.flags & dns.flags.AD:
            ad = "si"
        dump = str(response)
    except Exception as e:
        if "SERVFAIL" in str(e).upper():
            status = "SERVFAIL"
        dump = f"ERROR: {e}"
    return ad, status, dump


async def check_dnssec(domain, ro, outdir, ip, dnssec_resolvers=None):
    dk = await q(ro, domain, "DNSKEY")
    ds_a = await q(ro, domain, "DS")
    dk_pub = "si" if dk else "no"
    ds_pub = "si" if ds_a else "no"

    # --- Deteccion robusta del bit AD probando MULTIPLES resolvers ---
    # El bit AD depende del resolver validador. Se prueba contra una lista de
    # resolvers validadores conocidos. Si CUALQUIERA confirma el bit AD, la
    # cadena esta validada (Secure). Todo en una sola pasada -> una carpeta.
    if not dnssec_resolvers:
        dnssec_resolvers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]

    ad = "no"; status = "N/D"
    per_resolver_dump = []
    servfail_count = 0
    for rip in dnssec_resolvers:
        r_ad, r_status, r_dump = await _probe_ad_bit(domain, rip)
        per_resolver_dump.append(
            f"### Resolver {rip}\n# AD={r_ad}  status={r_status}\n{r_dump}\n")
        if r_status == "SERVFAIL":
            servfail_count += 1
        if r_ad == "si":
            ad = "si"
            if status in ("N/D", "SERVFAIL"):
                status = r_status
        elif status == "N/D":
            status = r_status

    all_servfail = (servfail_count == len(dnssec_resolvers))

    algos_local = []
    if dk:
        for r in dk:
            try:
                algos_local.append(str(r.algorithm))
            except Exception:
                pass
    algos_s = ",".join(sorted(set(algos_local))) if algos_local else "N/A"

    if all_servfail:
        diag = "Bogus (cadena rota)"
    elif dk_pub == "si" and ds_pub == "si" and ad == "si":
        diag = "Secure"
    elif dk_pub == "si" and ds_pub == "si" and ad == "no":
        diag = "Firmado (AD no confirmado)"
    elif dk_pub == "si" and ds_pub == "no":
        diag = "Incompleto (DS no publicado)"
    elif dk_pub == "no" and ds_pub == "no":
        diag = "No implementado"
    else:
        diag = "Inconsistente"

    write_evidence(outdir, domain, "dig_dnskey.txt", f"DNSKEY {domain}",
                   str(dk.rrset) if dk else "(empty)", ip)
    write_evidence(outdir, domain, "dig_ds.txt", f"DS {domain}",
                   str(ds_a.rrset) if ds_a else "(empty)", ip)
    write_evidence(outdir, domain, "dnssec_validation.txt",
                   f"make_query {domain} A +dnssec +ad (resolvers: {', '.join(dnssec_resolvers)})",
                   "\n".join(per_resolver_dump), ip)
    return {"dnskey_pub": dk_pub, "ds_pub": ds_pub, "ad_flag": ad, "status": status,
            "algos": algos_s, "diag": diag}


async def check_spf(domain, ro, outdir, ip):
    ans = await q(ro, domain, "TXT")
    txts = []
    if ans:
        for r in ans:
            try:
                txts.append(b"".join(r.strings).decode("utf-8", errors="replace"))
            except Exception:
                pass
    spfs = [t for t in txts if t.lower().startswith("v=spf1")]
    n = len(spfs); rec = spfs[0] if spfs else ""
    write_evidence(outdir, domain, "dig_txt.txt", f"TXT {domain}", "\n".join(txts), ip)
    r = {"pub": "no", "all": "N/A", "lookups": 0, "void": 0, "multi": "no", "len": 0, "providers": "", "record": ""}
    if not rec:
        return r
    r["pub"] = "si"; r["record"] = rec; r["len"] = len(rec)
    if " -all" in rec: r["all"] = "-all"
    elif " ~all" in rec: r["all"] = "~all"
    elif " ?all" in rec: r["all"] = "?all"
    elif " +all" in rec: r["all"] = "+all"
    else: r["all"] = "sin all"
    r["lookups"] = len(re.findall(r"(include:|a:|mx:|ptr:|exists:|redirect=)", rec))
    incs = re.findall(r"include:(\S+)", rec)
    void = 0; seen = []
    for inc in incs:
        sub = await q(ro, inc, "TXT")
        if not sub:
            void += 1
        low = inc.lower()
        if "spf.protection.outlook.com" in low: p = "Microsoft 365"
        elif "_spf.google.com" in low: p = "Google Workspace"
        elif "amazonses.com" in low: p = "Amazon SES"
        elif "mailgun" in low: p = "Mailgun"
        elif "sendgrid" in low: p = "SendGrid"
        elif "mailchimp" in low or "mcsv" in low: p = "Mailchimp"
        elif "hubspot" in low: p = "HubSpot"
        elif "zoho" in low: p = "Zoho Mail"
        elif "mandrill" in low: p = "Mandrill"
        elif "sparkpost" in low: p = "SparkPost"
        elif "postmark" in low: p = "Postmark"
        elif "mailjet" in low: p = "Mailjet"
        else: p = f"Otro: {inc}"
        if p not in seen:
            seen.append(p)
    r["void"] = void
    r["providers"] = "; ".join(seen)
    if n > 1: r["multi"] = "si"
    return r


async def check_dkim(domain, sels, ro, outdir, ip, counter, deep=False):
    """Prueba una lista de selectores DKIM contra el dominio.
    Devuelve dict con:
      - found: lista de selectores DKIM validos encontrados.
      - probed: cantidad de selectores probados.
      - deep: si se uso busqueda profunda.
    El diagnostico de 'no encontrado' se maneja en process_results para
    distinguir 'Sin DKIM' de 'No detectado entre selectores comunes'."""
    found = []
    probed = 0
    for sel in sels:
        probed += 1
        ans = await q(ro, f"{sel}._domainkey.{domain}", "TXT")
        if not ans:
            continue
        try:
            rec = "".join(b"".join(r.strings).decode("utf-8", errors="replace") for r in ans)
        except Exception:
            continue
        if "v=DKIM1" not in rec and "p=" not in rec:
            continue
        write_evidence(outdir, domain, f"dkim_{sel}.txt", f"TXT {sel}._domainkey.{domain}", rec, ip)
        mp = re.search(r"p=([A-Za-z0-9+/=]*)", rec)
        mk = re.search(r"k=([a-z0-9]+)", rec)
        mt = re.search(r"t=([ys]+)", rec)
        pv = mp.group(1) if mp else ""
        kv = mk.group(1) if mk else "rsa"
        tv = mt.group(1) if mt else "-"
        rev = "no"; bits = "N/D"
        if not pv:
            rev = "si (p= vacio)"
        else:
            try:
                der = base64.b64decode(pv)
                pk = serialization.load_der_public_key(der, backend=default_backend())
                bits = pk.key_size
            except Exception:
                bits = "N/D"
        srv = map_dkim_service(sel)
        est = derive_dkim_status(bits, tv, rev)
        sev = derive_dkim_severity(bits, tv, rev)
        counter[0] += 1
        found.append({"row": counter[0], "domain": domain, "selector": sel, "service": srv,
                      "record": rec, "algorithm": kv, "bits": bits if isinstance(bits, int) else "N/D",
                      "t_flag": tv, "revoked": rev, "estado": est, "severidad": sev})
    return {"found": found, "probed": probed, "deep": deep}


async def check_dmarc(domain, ro, outdir, ip):
    ans = await q(ro, f"_dmarc.{domain}", "TXT")
    rec = ""
    if ans:
        try:
            rec = "".join(b"".join(r.strings).decode("utf-8", errors="replace") for r in ans)
        except Exception:
            pass
    write_evidence(outdir, domain, "dig_dmarc.txt", f"TXT _dmarc.{domain}", rec or "(empty)", ip)
    r = {"pub": "no", "record": "", "p": "", "sp": "", "pct": "", "rua": "", "ruf": "",
         "aspf": "", "adkim": "", "fo": "", "rf": "", "ri": ""}
    if not rec or "v=DMARC1" not in rec:
        return r
    r["pub"] = "si"; r["record"] = rec

    def g(pat):
        mm = re.search(pat, rec)
        return mm.group(1) if mm else ""

    r["p"] = g(r"p=([a-z]+)")
    r["sp"] = g(r"sp=([a-z]+)")
    r["pct"] = g(r"pct=(\d+)") or "100"
    r["rua"] = g(r"rua=([^;]+)")
    r["ruf"] = g(r"ruf=([^;]+)")
    r["aspf"] = g(r"aspf=([rs])") or "r"
    r["adkim"] = g(r"adkim=([rs])") or "r"
    r["fo"] = g(r"fo=([01ds:]+)")
    r["rf"] = g(r"rf=([a-z]+)")
    r["ri"] = g(r"ri=(\d+)")
    return r


async def check_mx(domain, ro, outdir, ip):
    ans = await q(ro, domain, "MX")
    if not ans:
        write_evidence(outdir, domain, "dig_mx.txt", f"MX {domain}", "(empty)", ip)
        return {"records": "", "provider": "Sin MX"}
    records = sorted([(r.preference, str(r.exchange).rstrip(".")) for r in ans])
    rs = ";".join(f"{p} {h}" for p, h in records)
    write_evidence(outdir, domain, "dig_mx.txt", f"MX {domain}", rs, ip)
    low = rs.lower()
    if "mail.protection.outlook.com" in low: p = "Microsoft 365"
    elif "google.com" in low or "googlemail.com" in low: p = "Google Workspace"
    elif "zoho" in low: p = "Zoho Mail"
    elif "mimecast" in low: p = "Mimecast"
    elif "proofpoint" in low or "pphosted" in low: p = "Proofpoint"
    else: p = "Otro"
    return {"records": rs, "provider": p}


async def check_mta_sts(domain, ro, http, outdir, ip):
    ans = await q(ro, f"_mta-sts.{domain}", "TXT")
    txt = ""
    if ans:
        try:
            txt = "".join(b"".join(r.strings).decode("utf-8", errors="replace") for r in ans)
        except Exception:
            pass
    write_evidence(outdir, domain, "dig_mta_sts.txt", f"TXT _mta-sts.{domain}", txt or "(empty)", ip)
    r = {"pub": "no", "mode": "", "max_age": "", "mx": "", "accessible": "no"}
    if "v=STSv1" not in txt:
        return r
    r["pub"] = "si"
    try:
        url = f"https://mta-sts.{domain}/.well-known/mta-sts.txt"
        resp = await http.get(url, timeout=8.0)
        if resp.status_code == 200:
            body = resp.text
            write_evidence(outdir, domain, "mta_sts_policy.txt", f"GET {url}", body, ip)
            r["accessible"] = "si"
            for line in body.splitlines():
                low = line.strip().lower()
                if low.startswith("mode:"): r["mode"] = line.split(":", 1)[1].strip()
                elif low.startswith("max_age:"): r["max_age"] = line.split(":", 1)[1].strip()
                elif low.startswith("mx:"):
                    v = line.split(":", 1)[1].strip()
                    r["mx"] = (r["mx"] + ";" + v) if r["mx"] else v
    except Exception:
        pass
    return r


async def check_tls_rpt(domain, ro, outdir, ip):
    ans = await q(ro, f"_smtp._tls.{domain}", "TXT")
    txt = ""
    if ans:
        try:
            txt = "".join(b"".join(r.strings).decode("utf-8", errors="replace") for r in ans)
        except Exception:
            pass
    write_evidence(outdir, domain, "dig_tls_rpt.txt", f"TXT _smtp._tls.{domain}", txt or "(empty)", ip)
    r = {"pub": "no", "record": "", "rua": ""}
    if "v=TLSRPTv1" not in txt:
        return r
    r["pub"] = "si"; r["record"] = txt
    m = re.search(r"rua=([^;]+)", txt)
    if m:
        r["rua"] = m.group(1).strip()
    return r


async def check_bimi(domain, ro, http, outdir, ip):
    ans = await q(ro, f"default._bimi.{domain}", "TXT")
    txt = ""
    if ans:
        try:
            txt = "".join(b"".join(r.strings).decode("utf-8", errors="replace") for r in ans)
        except Exception:
            pass
    write_evidence(outdir, domain, "dig_bimi.txt", f"TXT default._bimi.{domain}", txt or "(empty)", ip)
    r = {"pub": "no", "record": "", "svg": "", "vmc_url": "", "vmc_status": "No aplica", "vmc_issuer": "", "vmc_exp": ""}
    if "v=BIMI1" not in txt:
        return r
    r["pub"] = "si"; r["record"] = txt
    ml = re.search(r"l=([^ ;]+)", txt)
    ma = re.search(r"a=([^ ;]+)", txt)
    if ml: r["svg"] = ml.group(1)
    if ma:
        r["vmc_url"] = ma.group(1); r["vmc_status"] = "No"
        try:
            resp = await http.get(r["vmc_url"], timeout=8.0)
            if resp.status_code == 200:
                pem = resp.content
                try:
                    cert = x509.load_pem_x509_certificate(pem, default_backend())
                except Exception:
                    cert = x509.load_der_x509_certificate(pem, default_backend())
                r["vmc_status"] = "Si"
                issuer_cn = ""
                for attr in cert.issuer:
                    if attr.oid._name == "commonName":
                        issuer_cn = attr.value
                        break
                r["vmc_issuer"] = issuer_cn or cert.issuer.rfc4514_string()
                try:
                    r["vmc_exp"] = cert.not_valid_after_utc.isoformat()
                except Exception:
                    r["vmc_exp"] = cert.not_valid_after.isoformat()
                (outdir / "evidencias" / domain / "bimi_vmc.pem").write_bytes(pem)
        except Exception:
            pass
    return r


async def audit_domain(domain, args, ro, http, outdir, counters, data, hallazgos):
    info = {"domain": domain}
    info.update(await check_whois(domain, outdir, args.resolver))
    info.update(await check_ns_soa(domain, ro, outdir, args.resolver))
    _dnssec_resolvers = [x.strip() for x in args.dnssec_resolvers.split(",") if x.strip()]
    info["dnssec"] = await check_dnssec(domain, ro, outdir, args.resolver,
                                        dnssec_resolvers=_dnssec_resolvers or None)
    info["spf"] = await check_spf(domain, ro, outdir, args.resolver)

    # --- Construccion de la lista de selectores DKIM ---
    sels = list(COMMON_SELECTORS)
    if args.deep_dkim:
        sels.extend(generate_deep_selectors(months_back=args.deep_months))
    if args.selectors:
        sels.extend(args.selectors.split())
    # Deduplicar preservando orden
    seen_sel = set(); sels_unique = []
    for x in sels:
        if x not in seen_sel:
            seen_sel.add(x); sels_unique.append(x)

    info["dkim_res"] = await check_dkim(domain, sels_unique, ro, outdir, args.resolver,
                                        counters["dkim_row"], deep=args.deep_dkim)
    info["dkim"] = info["dkim_res"]["found"]  # compat. con el resto del codigo
    info["dmarc"] = await check_dmarc(domain, ro, outdir, args.resolver)
    info["mx"] = await check_mx(domain, ro, outdir, args.resolver)
    info["mtasts"] = await check_mta_sts(domain, ro, http, outdir, args.resolver)
    info["tlsrpt"] = await check_tls_rpt(domain, ro, outdir, args.resolver)
    info["bimi"] = await check_bimi(domain, ro, http, outdir, args.resolver)
    process_results(domain, info, counters, data, hallazgos)
    return info


def process_results(domain, info, counters, data, hallazgos):
    s = info["spf"]; d = info["dmarc"]; ds = info["dnssec"]
    m = info["mx"]; mt = info["mtasts"]; tl = info["tlsrpt"]; bi = info["bimi"]
    dkim_res = info.get("dkim_res", {"found": info["dkim"], "probed": 0, "deep": False})
    counters["dom_num"] += 1
    n = counters["dom_num"]

    # SPF
    sst = derive_spf_status(s["pub"], s["all"], s["lookups"], s["void"], s["multi"])
    ssv = derive_spf_severity(s["pub"], s["all"], s["lookups"], s["void"], s["multi"])
    data["spf"].append([n, domain, s["record"], s["all"], s["lookups"], s["void"], s["len"],
                        s["providers"], s["multi"], sst, ssv])
    if s["multi"] == "si": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "SPF", "Multiples SPF", "Critica", "Consolidar"])
    if s["lookups"] > 10: hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "SPF", ">10 lookups", "Alta", "Reducir"])
    if s["all"] == "+all": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "SPF", "+all", "Critica", "Cambiar a -all"])
    if s["all"] in ("?all", "sin all"): hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "SPF", f"{s['all']}", "Alta", "Endurecer"])
    if s["pub"] == "no": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "SPF", "Sin SPF", "Alta", "Publicar"])

    # DKIM
    for r in info["dkim"]:
        data["dkim"].append([r["row"], r["domain"], r["selector"], r["service"], r["record"],
                            r["algorithm"], r["bits"], r["t_flag"], "Validar manualmente",
                            "Validar manualmente", "Validar manualmente", r["estado"], r["severidad"]])
        if isinstance(r["bits"], int):
            if r["bits"] < 1024: hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DKIM", f"<1024 bits {r['selector']}", "Critica", "Rotar"])
            elif r["bits"] < 2048: hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DKIM", f"<2048 bits {r['selector']}", "Alta", "Migrar 2048"])
    if not info["dkim"]:
        # Distinguir 'sin DKIM' de 'no detectado entre selectores probados'.
        if dkim_res.get("deep"):
            # Busqueda profunda ya realizada; probablemente selector muy custom.
            hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DKIM",
                              "No detectado ni en busqueda profunda (selector custom - verificar header DKIM-Signature)",
                              "Media", "Obtener selector real de un correo enviado y reauditar con --selectors"])
        else:
            hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DKIM",
                              "No detectado entre selectores comunes (puede existir con selector custom)",
                              "Media", "Reintentar con --deep-dkim o pasar el selector real con --selectors"])

    # DMARC
    dst = derive_dmarc_status(d["pub"], d["p"], d["sp"], d["pct"], d["rua"])
    dsv = derive_dmarc_severity(d["pub"], d["p"], d["sp"], d["pct"], d["rua"])
    data["dmarc"].append([n, domain, d["record"], d["p"], d["sp"], d["pct"], d["aspf"], d["adkim"],
                         d["rua"], d["ruf"], d["fo"], d["rf"], d["ri"], "", "", dst, dsv])
    if d["pub"] == "no": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DMARC", "Sin DMARC", "Critica", "Publicar"])
    elif d["p"] == "none": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DMARC", "p=none", "Alta", "Migrar"])
    elif d["p"] == "quarantine": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DMARC", "p=quarantine", "Media", "Migrar reject"])

    # DNSSEC
    nst = derive_dnssec_status(ds["diag"])
    nsv = derive_dnssec_severity(ds["diag"])
    data["dnssec"].append([n, domain, ds["dnskey_pub"], ds["ds_pub"], ds["ad_flag"], ds["status"],
                          ds["algos"], ds["diag"], nst, nsv])
    if ds["diag"].startswith("Bogus"): hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DNSSEC", "Cadena rota", "Critica", "Revisar DS"])
    elif ds["diag"].startswith("Incompleto"): hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DNSSEC", "Sin DS", "Alta", "Publicar DS"])
    elif ds["diag"] == "No implementado": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "DNSSEC", "Sin DNSSEC", "Media", "Activar"])

    # MTA-STS
    mst = derive_mtasts_status(mt["pub"], mt["mode"], mt["accessible"])
    counters["mtasts_ev"] += 1
    data["mtasts"].append([domain, mt["mode"] or "No publicado", mt["max_age"], mt["mx"],
                          mt["accessible"], mst, f"EV-MTASTS-{counters['mtasts_ev']:03d}", ""])
    if mt["pub"] == "no": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "MTA-STS", "No implementado", "Baja", "Publicar"])

    # TLS-RPT
    tst = derive_tlsrpt_status(tl["pub"], tl["rua"])
    counters["tlsrpt_ev"] += 1
    data["tlsrpt"].append([domain, tl["record"], tl["rua"], "", tst, f"EV-TLSRPT-{counters['tlsrpt_ev']:03d}", ""])
    if tl["pub"] == "no": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "TLS-RPT", "No implementado", "Baja", "Publicar"])

    # BIMI
    bst = derive_bimi_status(bi["pub"], bi["svg"], bi["vmc_status"])
    data["bimi"].append([domain, bi["record"], bi["svg"], bi["vmc_status"],
                        bi["vmc_issuer"], bi["vmc_exp"], bst, ""])
    if bi["pub"] == "si" and bi["vmc_status"] == "No": hallazgos.append([f"H-{len(hallazgos)+1:03d}", domain, "BIMI", "Sin VMC", "Informativa", "Adquirir"])

    # Remitentes autorizados
    provs = []; seen = set()
    if s["providers"]:
        for p in [x.strip() for x in s["providers"].split(";")]:
            if p and p not in seen:
                seen.add(p); provs.append(p)
    if m["provider"] and m["provider"] not in ("Sin MX", "Otro") and m["provider"] not in seen:
        seen.add(m["provider"]); provs.append(m["provider"])
    if not provs: provs = ["Por validar"]
    for prov in provs:
        prop = map_provider_purpose(prov)
        mec = map_provider_mechanism(prov)
        inc = "Si" if (s["providers"] and prov in s["providers"]) else "No"
        firma = "No"
        fw = prov.split()[0] if prov.split() else ""
        for dk in info["dkim"]:
            if fw.lower() in dk["service"].lower():
                firma = "Si"; break
        if d["pub"] == "no" or d["p"] == "none": ali = "No"
        elif inc == "Si" and firma == "Si": ali = "Si"
        elif inc == "Si" or firma == "Si": ali = "Parcial"
        else: ali = "No"
        est = derive_remit_state(inc, firma, ali)
        counters["remit_row"] += 1
        data["remit"].append([counters["remit_row"], domain, prov, prop, mec, inc, firma, ali,
                             "Validar manualmente", "Validar manualmente", est])

    # Cumplimiento global
    score = 0
    if s["pub"] == "si" and s["all"] in ("-all", "~all") and s["multi"] == "no" and s["lookups"] <= 10: score += 1
    if d["pub"] == "si" and d["p"] != "none": score += 1
    if ds["diag"] == "Secure" or ds["diag"].startswith("Firmado"): score += 1
    if mt["mode"] == "enforce": score += 1
    if tl["pub"] == "si": score += 1
    if bi["pub"] == "si": score += 1
    if info["dkim"]: score += 1
    pct = score * 100 // 7
    if pct >= 85: cumpl = f"Alto ({pct}%)"
    elif pct >= 50: cumpl = f"Medio ({pct}%)"
    else: cumpl = f"Bajo ({pct}%)"
    info["cumplimiento"] = cumpl; info["cumplimiento_pct"] = pct

    # Inventario y resumen
    data["inventario"].append([n, domain, "Produccion", "", info["registrar"], info["expires"],
                              "Si" if info["mx"]["provider"] != "Sin MX" else "No", "",
                              info["ns_provider"], ds["dnskey_pub"], ""])
    data["resumen"].append([domain, info["registrar"], info["created"], info["expires"], info["status"],
                           info["dnssec_whois"], info["ns_list"], info["soa_serial"], ds["diag"],
                           s["pub"], s["all"], s["lookups"], s["void"], s["multi"], d["pub"], d["p"],
                           d["sp"], d["pct"], d["rua"], m["provider"], mt["mode"] or "No publicado",
                           tl["pub"], bi["pub"], cumpl])


def build_excel(outdir, data, hallazgos, stats, args):
    wb = Workbook()
    thin = Side(border_style="thin", color="B7C9D6")
    BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
    F_TITLE = Font(name="Century Gothic", size=18, bold=True, color="FFFFFF")
    F_SUBT = Font(name="Century Gothic", size=12, bold=True, color="FFFFFF")
    F_H1 = Font(name="Century Gothic", size=11, bold=True, color="FFFFFF")
    F_H2 = Font(name="Century Gothic", size=10, bold=True, color="FFFFFF")
    F_LABEL = Font(name="Calibri", size=11, bold=True, color=C_NAVY)
    F_BODY = Font(name="Calibri", size=10, color="222222")
    FILL_TITLE = PatternFill("solid", fgColor=C_DARK)
    FILL_SUBT = PatternFill("solid", fgColor=C_MID)
    FILL_H1 = PatternFill("solid", fgColor=C_DARK)
    FILL_H2 = PatternFill("solid", fgColor=C_ACC)
    FILL_BAND = PatternFill("solid", fgColor=C_BAND)
    FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
    AC = Alignment(horizontal="center", vertical="center", wrap_text=True)
    AL = Alignment(horizontal="left", vertical="center", wrap_text=True)

    LIST_EST = '"Cumple,Cumple parcialmente,No cumple,No aplica,Pendiente"'
    LIST_SEV = '"Critica,Alta,Media,Baja,Informativa"'

    def style_header(ws, row, n_cols, fill=FILL_H1, font=F_H1):
        for c in range(1, n_cols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = fill; cell.font = font
            cell.alignment = AC; cell.border = BORDER
        ws.row_dimensions[row].height = 30

    def set_widths(ws, widths):
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

    def cf_status(ws, col, s, e):
        rng = f"{col}{s}:{col}{e}"
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Cumple"'],
            fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(color="006100")))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Cumple parcialmente"'],
            fill=PatternFill("solid", fgColor="FFEB9C"), font=Font(color="9C5700")))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"No cumple"'],
            fill=PatternFill("solid", fgColor="FFC7CE"), font=Font(color="9C0006", bold=True)))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"No aplica"'],
            fill=PatternFill("solid", fgColor="D9D9D9"), font=Font(color="555555")))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Pendiente"'],
            fill=PatternFill("solid", fgColor="DDEBF7"), font=Font(color="1F4E78")))

    def cf_sev(ws, col, s, e):
        rng = f"{col}{s}:{col}{e}"
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Critica"'],
            fill=PatternFill("solid", fgColor="C00000"), font=Font(color="FFFFFF", bold=True)))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Alta"'],
            fill=PatternFill("solid", fgColor="ED7D31"), font=Font(color="FFFFFF", bold=True)))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Media"'],
            fill=PatternFill("solid", fgColor="FFD966"), font=Font(color="7F5F00", bold=True)))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Baja"'],
            fill=PatternFill("solid", fgColor="A9D08E"), font=Font(color="375623")))
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Informativa"'],
            fill=PatternFill("solid", fgColor="D9D9D9"), font=Font(color="555555")))

    # Portada
    ws = wb.active; ws.title = "Portada"
    ws.sheet_view.showGridLines = False
    set_widths(ws, [3, 32, 70, 4])
    ws.merge_cells("B2:C2")
    ws["B2"] = "Auditoria de Autenticacion de Correo Electronico"
    ws["B2"].font = F_TITLE; ws["B2"].fill = FILL_TITLE; ws["B2"].alignment = AC
    ws.row_dimensions[2].height = 44
    ws.merge_cells("B3:C3")
    ws["B3"] = "SPF / DKIM / DMARC + Controles Complementarios"
    ws["B3"].font = F_SUBT; ws["B3"].fill = FILL_SUBT; ws["B3"].alignment = AC
    ws.row_dimensions[3].height = 28
    portada = [
        ("Version del documento", "3.2"),
        ("Fecha de ejecucion", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Elaborado por", "Eduardo Recinos"),
        ("Cargo", "VCISO"),
        ("Resolver DNS utilizado", args.resolver),
        ("Modo DKIM", "Profundo (--deep-dkim)" if args.deep_dkim else "Balanceado (comun)"),
        ("Total de dominios auditados", str(stats["total_domains"])),
        ("Total de hallazgos", str(stats["total_findings"])),
        ("Marco de referencia", "ISO/IEC 27001:2022 A.5.14, A.8.20, A.8.21, A.8.23 - NIST CSF 2.0 - NIST SP 800-177 Rev.1 - M3AAWG - RFC 7208/6376/7489/8460/8461"),
        ("Convenciones de Estado", "Cumple - Cumple parcialmente - No cumple - No aplica - Pendiente"),
        ("Convenciones de Severidad", "Critica - Alta - Media - Baja - Informativa"),
    ]
    r = 5
    for lbl, val in portada:
        c1 = ws.cell(row=r, column=2, value=lbl); c1.font = F_LABEL; c1.fill = FILL_BAND; c1.alignment = AL; c1.border = BORDER
        c2 = ws.cell(row=r, column=3, value=val); c2.font = F_BODY; c2.alignment = AL; c2.border = BORDER
        ws.row_dimensions[r].height = 42 if len(val) > 80 else 22
        r += 1

    def add_sheet(name, headers, rows, status_col=None, sev_col=None, col_widths=None):
        ws = wb.create_sheet(name)
        for i, h in enumerate(headers, start=1):
            ws.cell(row=1, column=i, value=h)
        style_header(ws, 1, len(headers))
        for ri, row in enumerate(rows, start=2):
            for ci, val in enumerate(row, start=1):
                cell = ws.cell(row=ri, column=ci, value=val)
                cell.font = F_BODY; cell.alignment = AL; cell.border = BORDER
                cell.fill = FILL_BAND if ri % 2 == 0 else FILL_WHITE
            ws.row_dimensions[ri].height = 22
        if col_widths:
            set_widths(ws, col_widths)
        ws.freeze_panes = "A2"
        end = max(2, 1 + len(rows))
        if status_col:
            dv = DataValidation(type="list", formula1=LIST_EST, allow_blank=True)
            ws.add_data_validation(dv)
            dv.add(f"{status_col}2:{status_col}{end}")
            cf_status(ws, status_col, 2, end)
        if sev_col:
            dv = DataValidation(type="list", formula1=LIST_SEV, allow_blank=True)
            ws.add_data_validation(dv)
            dv.add(f"{sev_col}2:{sev_col}{end}")
            cf_sev(ws, sev_col, 2, end)
        return ws

    add_sheet("Inventario_Dominios",
        ["#", "Dominio", "Tipo", "Marca / Empresa", "Registrar", "Fecha de expiracion",
         "Envia correo", "Propietario interno", "DNS gestionado por", "DNSSEC", "Comentarios"],
        data["inventario"],
        col_widths=[5, 28, 16, 22, 22, 18, 12, 22, 22, 12, 40])

    add_sheet("SPF",
        ["#", "Dominio", "Registro SPF (texto completo)", "Mecanismo all", "DNS lookups",
         "Void lookups", "Longitud (chars)", "Proveedores autorizados incluidos",
         "Multiples registros SPF", "Estado", "Severidad"],
        data["spf"], status_col="J", sev_col="K",
        col_widths=[5, 26, 55, 14, 12, 12, 14, 35, 14, 22, 14])

    add_sheet("DKIM",
        ["#", "Dominio", "Selector", "Servicio que firma", "Registro publico (texto)",
         "Algoritmo", "Tamano de llave (bits)", "Flag t=y (modo prueba)",
         "Fecha de creacion", "Ultima rotacion", "Proxima rotacion", "Estado", "Severidad"],
        data["dkim"], status_col="L", sev_col="M",
        col_widths=[5, 24, 20, 24, 50, 14, 14, 14, 16, 16, 16, 22, 14])

    add_sheet("DMARC",
        ["#", "Dominio", "Registro DMARC", "Politica p=", "Politica sp=", "pct=", "aspf=",
         "adkim=", "RUA", "RUF", "fo=", "rf=", "ri=", "Recibiendo reportes",
         "Plataforma de analisis", "Estado", "Severidad"],
        data["dmarc"], status_col="P", sev_col="Q",
        col_widths=[5, 24, 50, 14, 14, 8, 14, 14, 28, 28, 10, 10, 10, 16, 22, 22, 14])

    add_sheet("DNSSEC",
        ["#", "Dominio", "DNSKEY publicado", "DS en zona padre", "Bit AD validador",
         "Status resolver", "Algoritmos", "Diagnostico", "Estado", "Severidad"],
        data["dnssec"], status_col="I", sev_col="J",
        col_widths=[5, 24, 16, 16, 16, 16, 16, 30, 22, 14])

    # Complementos (MTA-STS, TLS-RPT, BIMI)
    ws = wb.create_sheet("Complementos")
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:H1")
    ws["A1"] = "MTA-STS"; ws["A1"].font = F_SUBT; ws["A1"].fill = FILL_SUBT; ws["A1"].alignment = AC
    ws.row_dimensions[1].height = 26
    mta_hdr = ["Dominio", "Politica publicada", "max_age", "Hosts MX listados",
               "Archivo /.well-known/mta-sts.txt accesible", "Estado", "Evidencia (ID)", "Comentarios"]
    for i, h in enumerate(mta_hdr, start=1):
        ws.cell(row=2, column=i, value=h)
    style_header(ws, 2, len(mta_hdr), fill=FILL_H2, font=F_H2)
    for ri, row in enumerate(data["mtasts"], start=3):
        for ci, val in enumerate(row, start=1):
            c = ws.cell(row=ri, column=ci, value=val)
            c.font = F_BODY; c.alignment = AL; c.border = BORDER
            c.fill = FILL_BAND if ri % 2 == 1 else FILL_WHITE
    mta_end = max(3, 2 + len(data["mtasts"]))
    if data["mtasts"]:
        dv = DataValidation(type="list", formula1=LIST_EST, allow_blank=True); ws.add_data_validation(dv)
        dv.add(f"F3:F{mta_end}"); cf_status(ws, "F", 3, mta_end)
    tls_start = mta_end + 3
    ws.merge_cells(f"A{tls_start}:G{tls_start}")
    ws[f"A{tls_start}"] = "TLS-RPT"; ws[f"A{tls_start}"].font = F_SUBT
    ws[f"A{tls_start}"].fill = FILL_SUBT; ws[f"A{tls_start}"].alignment = AC
    ws.row_dimensions[tls_start].height = 26
    tls_hdr = ["Dominio", "Registro _smtp._tls TXT", "Buzon rua de reportes",
               "Recibiendo reportes", "Estado", "Evidencia (ID)", "Comentarios"]
    for i, h in enumerate(tls_hdr, start=1):
        ws.cell(row=tls_start + 1, column=i, value=h)
    style_header(ws, tls_start + 1, len(tls_hdr), fill=FILL_H2, font=F_H2)
    for ri, row in enumerate(data["tlsrpt"], start=tls_start + 2):
        for ci, val in enumerate(row, start=1):
            c = ws.cell(row=ri, column=ci, value=val)
            c.font = F_BODY; c.alignment = AL; c.border = BORDER
            c.fill = FILL_BAND if ri % 2 == 1 else FILL_WHITE
    tls_end = max(tls_start + 2, tls_start + 1 + len(data["tlsrpt"]))
    if data["tlsrpt"]:
        dv = DataValidation(type="list", formula1=LIST_EST, allow_blank=True); ws.add_data_validation(dv)
        dv.add(f"E{tls_start+2}:E{tls_end}"); cf_status(ws, "E", tls_start + 2, tls_end)
    bimi_start = tls_end + 3
    ws.merge_cells(f"A{bimi_start}:H{bimi_start}")
    ws[f"A{bimi_start}"] = "BIMI"; ws[f"A{bimi_start}"].font = F_SUBT
    ws[f"A{bimi_start}"].fill = FILL_SUBT; ws[f"A{bimi_start}"].alignment = AC
    ws.row_dimensions[bimi_start].height = 26
    bimi_hdr = ["Dominio", "Registro default._bimi", "URL del SVG", "Certificado VMC",
                "Autoridad emisora", "Expiracion VMC", "Estado", "Comentarios"]
    for i, h in enumerate(bimi_hdr, start=1):
        ws.cell(row=bimi_start + 1, column=i, value=h)
    style_header(ws, bimi_start + 1, len(bimi_hdr), fill=FILL_H2, font=F_H2)
    for ri, row in enumerate(data["bimi"], start=bimi_start + 2):
        for ci, val in enumerate(row, start=1):
            c = ws.cell(row=ri, column=ci, value=val)
            c.font = F_BODY; c.alignment = AL; c.border = BORDER
            c.fill = FILL_BAND if ri % 2 == 1 else FILL_WHITE
    bimi_end = max(bimi_start + 2, bimi_start + 1 + len(data["bimi"]))
    if data["bimi"]:
        dv = DataValidation(type="list", formula1=LIST_EST, allow_blank=True); ws.add_data_validation(dv)
        dv.add(f"G{bimi_start+2}:G{bimi_end}"); cf_status(ws, "G", bimi_start + 2, bimi_end)
    set_widths(ws, [24, 30, 28, 18, 28, 18, 16, 30])

    add_sheet("Remitentes_Autorizados",
        ["#", "Dominio", "Servicio / Proveedor", "Proposito", "Mecanismo de envio",
         "Incluido en SPF", "Firma DKIM propia", "Alineacion DMARC",
         "Propietario interno del servicio", "Fecha de alta", "Estado"],
        data["remit"], status_col="K",
        col_widths=[5, 24, 24, 26, 22, 14, 16, 18, 28, 16, 22])

    add_sheet("Hallazgos",
        ["ID Hallazgo", "Dominio afectado", "Control", "Descripcion del hallazgo",
         "Severidad", "Recomendacion"],
        hallazgos, sev_col="E",
        col_widths=[14, 24, 14, 55, 14, 45])

    add_sheet("Resumen_Consolidado",
        ["dominio", "registrar", "creado", "expira", "estado_dominio", "whois_dnssec",
         "ns_actuales", "soa_serial", "dnssec_estado", "spf_publicado", "spf_all",
         "spf_lookups", "spf_void", "spf_multi", "dmarc_pub", "dmarc_p", "dmarc_sp",
         "dmarc_pct", "dmarc_rua", "mx_proveedor", "mta_sts", "tls_rpt", "bimi", "cumplimiento"],
        data["resumen"],
        col_widths=[24, 22, 18, 18, 22, 12, 30, 12, 24, 12, 12, 12, 12, 12, 12, 12, 12, 8, 28, 18, 16, 12, 8, 18])

    # Evidencias_Index
    ws = wb.create_sheet("Evidencias_Index")
    hdr = ["Dominio", "Archivo de evidencia", "Ruta relativa"]
    for i, h in enumerate(hdr, start=1):
        ws.cell(row=1, column=i, value=h)
    style_header(ws, 1, len(hdr))
    ev_dir = outdir / "evidencias"
    rr = 2
    if ev_dir.exists():
        for dom_dir in sorted(ev_dir.iterdir()):
            if dom_dir.is_dir():
                for f in sorted(dom_dir.iterdir()):
                    ws.cell(row=rr, column=1, value=dom_dir.name)
                    ws.cell(row=rr, column=2, value=f.name)
                    ws.cell(row=rr, column=3, value=str(f.relative_to(outdir)))
                    for c in range(1, 4):
                        cell = ws.cell(row=rr, column=c)
                        cell.font = F_BODY; cell.alignment = AL; cell.border = BORDER
                        cell.fill = FILL_BAND if rr % 2 == 0 else FILL_WHITE
                    rr += 1
    set_widths(ws, [24, 30, 50])
    ws.freeze_panes = "A2"

    excel_name = args.excel_name or f"Auditoria_Email_Authentication_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_path = outdir / excel_name
    wb.save(excel_path)
    return excel_path


def banner():
    art = (f"[bold {NM}]╔══════════════════════════════════════════════════════════════╗[/]\n"
           f"[bold {NM}]║[/]  [bold {NC}]E M A I L[/]  [bold {NG}]D N S[/]  [bold {NO}]A U D I T[/]  [bold {NY}]v 3 . 2[/]            [bold {NM}]║[/]\n"
           f"[bold {NM}]║[/]  [{NP} italic]Excel Unificado con Paleta Corporativa[/]                [bold {NM}]║[/]\n"
           f"[bold {NM}]╚══════════════════════════════════════════════════════════════╝[/]\n"
           f"  [{NC}]Autor:[/] [bold {NY}]Eduardo Recinos[/]   [{NC}]CISO:[/] [bold {NG}]VCISO[/]   "
           f"[{NC}]Fecha:[/] [bold {NO}]2026-06-30[/]")
    return Panel(art, border_style=NM, box=DOUBLE, padding=(0, 1))


def status_bar(domain, idx, total, findings, start):
    el = int(time.time() - start); mins, secs = divmod(el, 60)
    pct = (idx / total * 100) if total else 0
    bl = 30; fl = int(bl * idx / total) if total else 0
    bar = f"[{NG}]" + "█" * fl + "[/][grey50]" + "░" * (bl - fl) + "[/]"
    return Panel(f"[{NC}]▶[/] [bold {NY}]{domain}[/]   {bar} [bold {NM}]{idx}/{total}[/] "
                 f"([bold {NG}]{pct:.0f}%[/])   [{NO}]Hallazgos:[/] [bold {NR}]{findings}[/]   "
                 f"[{NP}]Tiempo:[/] [bold {NC}]{mins:02d}:{secs:02d}[/]",
                 border_style=NC, box=ROUNDED, padding=(0, 1))


def render_panel(info):
    s = info["spf"]; dm = info["dmarc"]; dns_d = info["dnssec"]
    mt = info["mtasts"]; tl = info["tlsrpt"]; bi = info["bimi"]
    dkim_res = info.get("dkim_res", {"found": info["dkim"], "probed": 0, "deep": False})
    cumpl = info.get("cumplimiento", "N/D"); pct = info.get("cumplimiento_pct", 0)
    color = NG if pct >= 85 else NY if pct >= 50 else NR
    t = Table(box=HEAVY, border_style=NP, show_header=True,
              header_style=Style(color=NM, bold=True))
    t.add_column("Control", style=Style(color=NC, bold=True), width=12)
    t.add_column("Estado", width=56)

    def cell(x, l):
        if l == "ok": return f"[{NG}]✔ {x}[/]"
        if l == "warn": return f"[{NY}]◐ {x}[/]"
        if l == "fail": return f"[{NR}]✘ {x}[/]"
        return f"[grey50]· {x}[/]"

    # SPF
    if s["pub"] == "si":
        if s["all"] in ("-all", "~all") and s["multi"] == "no" and s["lookups"] <= 10:
            t.add_row("SPF", cell(f"{s['all']} · lookups={s['lookups']}", "ok"))
        else:
            t.add_row("SPF", cell(f"{s['all']} · lookups={s['lookups']}", "warn"))
    else:
        t.add_row("SPF", cell("No publicado", "fail"))

    # DKIM — mensaje diferenciado
    if info["dkim"]:
        sels = ", ".join([f"{r['selector']}({r['bits']})" for r in info["dkim"][:3]])
        if len(info["dkim"]) > 3:
            sels += f" +{len(info['dkim'])-3}"
        t.add_row("DKIM", cell(sels, "ok"))
    else:
        if dkim_res.get("deep"):
            t.add_row("DKIM", cell(f"No detectado (busqueda profunda, {dkim_res.get('probed',0)} selectores)", "warn"))
        else:
            t.add_row("DKIM", cell("No detectado entre comunes (probar --deep-dkim)", "warn"))

    # DMARC
    if dm["pub"] == "si":
        lvl = "ok" if dm["p"] == "reject" else "warn" if dm["p"] == "quarantine" else "fail"
        t.add_row("DMARC", cell(f"p={dm['p']} pct={dm['pct']}", lvl))
    else:
        t.add_row("DMARC", cell("No publicado", "fail"))

    # DNSSEC
    diag = dns_d["diag"]
    lvl = "ok" if (diag == "Secure" or diag.startswith("Firmado")) else "warn" if diag.startswith("Incompleto") else "fail"
    t.add_row("DNSSEC", cell(diag, lvl))

    # MTA-STS
    if mt["mode"] == "enforce":
        t.add_row("MTA-STS", cell("enforce", "ok"))
    elif mt["mode"] == "testing":
        t.add_row("MTA-STS", cell("testing", "warn"))
    else:
        t.add_row("MTA-STS", cell("No publicado", "fail"))

    # TLS-RPT
    t.add_row("TLS-RPT", cell("Publicado" if tl["pub"] == "si" else "No publicado",
                              "ok" if tl["pub"] == "si" else "fail"))

    # BIMI
    if bi["pub"] == "si":
        lvl = "ok" if bi["vmc_status"] == "Si" else "warn"
        t.add_row("BIMI", cell(f"VMC={bi['vmc_status']}", lvl))
    else:
        t.add_row("BIMI", cell("No publicado", "fail"))

    # MX
    t.add_row("MX", cell(info["mx"]["provider"],
                        "ok" if info["mx"]["provider"] not in ("Sin MX", "Otro") else "warn"))

    title = f"[bold {NC}]▶ {info['domain']}[/]   [bold {color}]{cumpl}[/]"
    return Panel(t, title=title, border_style=color, box=DOUBLE, padding=(0, 1))


def final_panel(stats, paths, elapsed):
    mins, secs = divmod(int(elapsed), 60)
    sev_t = Table(box=ROUNDED, border_style=NP, show_header=True,
                  header_style=Style(color=NM, bold=True))
    sev_t.add_column("Severidad", style=Style(color=NC, bold=True))
    sev_t.add_column("Cantidad", justify="right")
    colors = {"Critica": NR, "Alta": NO, "Media": NY, "Baja": NG, "Informativa": "grey70"}
    for sev in ["Critica", "Alta", "Media", "Baja", "Informativa"]:
        n = stats["sev_count"].get(sev, 0)
        sev_t.add_row(f"[{colors[sev]}]{sev}[/]", f"[{colors[sev]}]{n}[/]")
    body = (f"[bold {NC}]Dominios auditados:[/] [bold {NG}]{stats['total_domains']}[/]\n"
            f"[bold {NC}]Tiempo total:[/] [bold {NO}]{mins:02d}:{secs:02d}[/]\n"
            f"[bold {NC}]Excel unificado:[/] [bold {NY}]{paths['excel']}[/]\n"
            f"[bold {NC}]Carpeta evidencias:[/] [bold {NY}]{paths['evidencias']}[/]")
    return Panel(body, title=f"[bold {NM}]✦ AUDITORIA COMPLETA ✦[/]",
                 border_style=NM, box=DOUBLE, padding=(1, 2))


async def run_audit(args):
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "evidencias").mkdir(exist_ok=True)
    with open(args.domains, "r", encoding="utf-8") as f:
        domains = [l.strip().lower() for l in f if l.strip() and not l.strip().startswith("#")]
    if not domains:
        console.print(f"[{NR}]ERROR: Sin dominios.[/]")
        return
    data = {k: [] for k in ["spf", "dkim", "dmarc", "dnssec", "mtasts", "tlsrpt", "bimi", "remit", "resumen", "inventario"]}
    hallazgos = []
    ro = dns.asyncresolver.Resolver()
    ro.nameservers = [args.resolver]; ro.timeout = 5; ro.lifetime = 8
    http = httpx.AsyncClient(verify=True, follow_redirects=True)
    counters = {"dom_num": 0, "dkim_row": [0], "mtasts_ev": 0, "tlsrpt_ev": 0, "remit_row": 0}
    stats = {"total_domains": 0, "total_findings": 0, "sev_count": {}}
    start = time.time()
    console.print(banner())
    if args.deep_dkim:
        console.print(f"[{NY}][*] Modo DKIM PROFUNDO activado (--deep-dkim, {args.deep_months} meses de selectores rotativos)[/]")
    console.print()
    for i, domain in enumerate(domains, 1):
        try:
            console.print(status_bar(domain, i - 1, len(domains), len(hallazgos), start))
            info = await audit_domain(domain, args, ro, http, outdir, counters, data, hallazgos)
            console.print(render_panel(info)); console.print()
        except Exception as e:
            console.print(f"[{NR}]ERROR {domain}: {e}[/]")
            continue
    for h in hallazgos:
        sev = h[4]
        stats["sev_count"][sev] = stats["sev_count"].get(sev, 0) + 1
    stats["total_domains"] = len(domains)
    stats["total_findings"] = len(hallazgos)
    elapsed = time.time() - start
    excel_path = build_excel(outdir, data, hallazgos, stats, args)
    await http.aclose()
    console.print(final_panel(stats, {"excel": excel_path.absolute(),
                                      "evidencias": (outdir / "evidencias").absolute()}, elapsed))
    console.print()
    console.print(Align.center(f"[italic {NP}]Auditoria completada · "
                              f"[bold {NY}]Eduardo Recinos[/] · VCISO[/]"))
    console.print()


def parse_args():
    p = argparse.ArgumentParser(description="Email DNS Audit v3.2 - Excel Unificado",
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--domains", "-d", help="Archivo con dominios")
    p.add_argument("--selectors", "-s", default="", help="Selectores DKIM extra (separados por espacio)")
    p.add_argument("--deep-dkim", action="store_true",
                   help="Busqueda DKIM PROFUNDA: agrega selectores rotativos por fecha "
                        "(Google, Amazon SES, SparkPost, Postmark, etc.) y muchos mas "
                        "proveedores. Mas lento pero mayor deteccion.")
    p.add_argument("--deep-months", type=int, default=30,
                   help="Meses hacia atras para generar selectores rotativos por fecha "
                        "en modo --deep-dkim (default 30).")
    p.add_argument("--resolver", "-r", default="1.1.1.1",
                   help="Resolver DNS para consultas generales (default 1.1.1.1)")
    p.add_argument("--dnssec-resolvers", default="1.1.1.1,8.8.8.8,9.9.9.9",
                   help="Resolvers validadores para el bit AD de DNSSEC, separados por coma "
                        "(default: 1.1.1.1,8.8.8.8,9.9.9.9). Si cualquiera valida, es Secure.")
    p.add_argument("--output", "-o", default=f"./audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                   help="Directorio salida")
    p.add_argument("--excel-name", default="", help="Nombre del Excel")
    p.add_argument("--install-deps", action="store_true")
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    if not args.domains:
        console.print(f"[{NR}]ERROR: --domains requerido[/]")
        sys.exit(1)
    if not Path(args.domains).is_file():
        console.print(f"[{NR}]ERROR: No existe {args.domains}[/]")
        sys.exit(1)
    try:
        asyncio.run(run_audit(args))
    except KeyboardInterrupt:
        console.print(f"\n[{NR}]Interrumpido.[/]")
        sys.exit(130)


if __name__ == "__main__":
    main()
