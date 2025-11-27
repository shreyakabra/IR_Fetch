from ..models import Intent
import re
import os
import json
import logging
from typing import List, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

ALL_DOC_TYPES = [
    "annual report",
    "earnings release",          # quarterly / half-yearly / semi-annual reports
    "investor presentation",     # presentations / slide decks
    "financial statements",      # full financial statements
]

DEFAULT_DOC_TYPES = ["annual report"]

def _regex_parse(prompt: str) -> Intent:
    """Fallback regex parser (original implementation)"""
    t = prompt.strip()
    
    # Simple doc type extraction
    txt = t.lower()
    doc_types = []
    if "annual" in txt or "10-k" in txt:
        doc_types.append("annual report")
    if "quarter" in txt or "10-q" in txt or "earnings" in txt:
        doc_types.append("earnings release")
    if "presentation" in txt or "deck" in txt:
        doc_types.append("investor presentation")
        
    if not doc_types:
        doc_types = DEFAULT_DOC_TYPES.copy()
        
    # Simple company extraction
    tokens = [w for w in re.findall(r"[A-Za-z&.\-]+", t) if len(w) > 1]
    common = set("download latest report reports annual quarterly from the of to and get all files filings documents".split())
    cand = [w for w in tokens if w.lower() not in common]
    company = cand[0] if cand else "Unknown"
    
    # Years
    years = sorted({int(y) for y in re.findall(r"(20\d{2})", t)})
    
    # Extras
    extras = {}
    if "q1" in txt: extras["quarter"] = "Q1"
    elif "q2" in txt: extras["quarter"] = "Q2"
    elif "q3" in txt: extras["quarter"] = "Q3"
    elif "q4" in txt: extras["quarter"] = "Q4"
    
    return Intent(company=company, doc_type=doc_types[0], doc_types=doc_types, years=years, extras=extras)

def parse_prompt(prompt: str) -> Intent:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found, using regex fallback parser")
        return _regex_parse(prompt)
        
    try:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """You are a financial document parser. Extract the following from the user prompt:
1. company: The company name (e.g. "Apple", "Tesla", "Johnson & Johnson").
2. doc_types: List of document types wanted. Map to: "annual report", "earnings release", "investor presentation", "financial statements". Default to ["annual report"] if unclear.
3. years: List of years mentioned (e.g. [2022, 2023]). If "last 3 years", calculate them relative to current year.
4. extras: Dictionary with "quarter" (Q1-Q4) or "half" (H1-H2) if specified.

Return JSON only."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        company = data.get("company", "Unknown")
        doc_types = data.get("doc_types", DEFAULT_DOC_TYPES)
        years = data.get("years", [])
        extras = data.get("extras", {})
        
        # Ensure doc_types is a list and has valid values
        if isinstance(doc_types, str):
            doc_types = [doc_types]
        
        # Map to standard types if needed (LLM usually does this, but safety check)
        valid_types = set(ALL_DOC_TYPES)
        cleaned_types = []
        for dt in doc_types:
            dt_lower = dt.lower()
            if "annual" in dt_lower or "10-k" in dt_lower: cleaned_types.append("annual report")
            elif "quarter" in dt_lower or "earnings" in dt_lower: cleaned_types.append("earnings release")
            elif "presentation" in dt_lower: cleaned_types.append("investor presentation")
            else: cleaned_types.append(dt) # Keep original if no match, or filter?
            
        if not cleaned_types:
            cleaned_types = DEFAULT_DOC_TYPES
            
        return Intent(
            company=company,
            doc_type=cleaned_types[0],
            doc_types=cleaned_types,
            years=years,
            extras=extras
        )
        
    except Exception as e:
        logger.error(f"OpenAI parsing failed: {e}, falling back to regex")
        return _regex_parse(prompt)

