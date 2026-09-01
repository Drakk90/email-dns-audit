# Attack Surface Detector Specification

## Purpose
Offline algorithmic detection of lookalike domains (typosquatting, bit-squatting, homoglyphs) and dangling DNS records vulnerable to Subdomain Takeover.

## Requirements

### Requirement: Local Typosquatting and Homoglyph Generation
The system MUST generate domain permutations using Levenshtein distance, vowel swaps, bit-flips, and Unicode confusable characters without external APIs.

#### Scenario: Typosquat candidate discovery
- GIVEN a primary corporate domain `example.com`
- WHEN the detector runs permutation algorithms
- THEN the system MUST produce lookalike candidates (e.g. `examp1e.com`, `exampel.com`)
- AND check DNS A/MX resolution to identify actively registered threats.

### Requirement: Dangling CNAME Subdomain Takeover Detection
The system MUST resolve discovered CNAME records and match unresponsive target hostnames against a signature database of 50+ third-party service providers.

#### Scenario: Unclaimed S3 bucket CNAME
- GIVEN a subdomain `assets.example.com` with a CNAME pointing to an unallocated AWS S3 bucket
- WHEN the detector evaluates HTTP responses and DNS resolution
- THEN the system MUST detect the dangling CNAME signature
- AND flag a critical vulnerability.
