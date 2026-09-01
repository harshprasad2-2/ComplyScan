"""
ComplyScan Declaration Extraction Module
Extracts structured fields from OCR text using regex and keyword matching.
"""

import re
from typing import List, Dict, Any
from modules.config import COMPLIANCE_RULES

class DeclarationExtractor:
    """Extracts declaration fields from OCR results."""
    
    def __init__(self):
        self.anchor_phrases = {
            'manufacturer': ['mfd by', 'manufactured by', 'packed by', 'mkd by', 'made by'],
            'packer': ['packed by', 'packer', 'pkl by'],
            'importer': ['imported by', 'imp by', 'importer'],
            'consumer_care': ['customer care', 'consumer care', 'support', 'contact us', 'call'],
        }
    
    def extract_all_fields(self, ocr_results: List[Dict]) -> Dict[str, Any]:
        """
        Extract all compliance fields from OCR results.
        
        Args:
            ocr_results (list): List of OCR detections from ocr_engine
        
        Returns:
            dict: Dictionary of extracted fields with their properties
        """
        # Combine all OCR text
        full_text = ' '.join([r['text'] for r in ocr_results])
        full_text_lower = full_text.lower()
        
        fields = {
            'manufacturer': self._extract_manufacturer(full_text, ocr_results),
            'commodity_name': self._extract_commodity_name(full_text, ocr_results),
            'net_quantity': self._extract_net_quantity(full_text, ocr_results),
            'manufacture_or_pack_date': self._extract_date(full_text, ocr_results),
            'mrp': self._extract_mrp(full_text, ocr_results),
            'mrp_inclusive_tax': self._extract_mrp_inclusive_tax(full_text, ocr_results),
            'consumer_care_contact': self._extract_consumer_care(full_text, ocr_results),
            'country_of_origin': self._extract_country_of_origin(full_text, ocr_results),
        }
        
        return fields
    
    def _extract_manufacturer(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract manufacturer/packer/importer information."""
        return self._extract_by_anchor_phrase(text, ocr_results, self.anchor_phrases['manufacturer'])
    
    def _extract_commodity_name(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract commodity name."""
        # Look for common commodity names
        commodity_keywords = ['rice', 'wheat', 'cereal', 'oil', 'salt', 'sugar', 'flour', 
                            'milk', 'tea', 'coffee', 'spice', 'lentil', 'bean', 'soup']
        
        text_lower = text.lower()
        for keyword in commodity_keywords:
            if keyword in text_lower:
                # Find the OCR result containing this keyword and boost confidence
                for result in ocr_results:
                    if keyword in result['text'].lower():
                        return {
                            'value': keyword.title(),
                            'confidence': result['confidence'] * 0.95,  # High confidence for keyword match
                            'evidence_text': result['text'],
                            'status': 'found',
                            'extraction_method': 'keyword_match'
                        }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_net_quantity(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract net quantity (weight/volume/count)."""
        pattern = r'(\d+(?:\.\d+)?)\s*(g|kg|mg|ml|l|litre|liter|no\.?|number|count)'
        
        for result in ocr_results:
            match = re.search(pattern, result['text'], re.IGNORECASE)
            if match:
                return {
                    'value': f"{match.group(1)} {match.group(2)}",
                    'confidence': result['confidence'],
                    'evidence_text': result['text'],
                    'bbox': result['bbox'],
                    'status': 'found',
                    'extraction_method': 'regex'
                }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_date(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract manufacture/packing date in MM/YYYY format."""
        pattern = r'(0[1-9]|1[0-2])/(\d{4})'
        
        for result in ocr_results:
            match = re.search(pattern, result['text'])
            if match:
                # Verify it's not a future date
                import datetime
                month, year = int(match.group(1)), int(match.group(2))
                current_year = datetime.datetime.now().year
                
                if year <= current_year:
                    return {
                        'value': f"{match.group(1)}/{match.group(2)}",
                        'confidence': result['confidence'],
                        'evidence_text': result['text'],
                        'bbox': result['bbox'],
                        'status': 'found',
                        'extraction_method': 'regex'
                    }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_mrp(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract Maximum Retail Price (MRP)."""
        pattern = r'(Rs\.?|₹|INR)\s*(\d+(?:\.\d+)?)'
        
        for result in ocr_results:
            match = re.search(pattern, result['text'], re.IGNORECASE)
            if match:
                return {
                    'value': f"₹{match.group(2)}",
                    'confidence': result['confidence'],
                    'evidence_text': result['text'],
                    'bbox': result['bbox'],
                    'status': 'found',
                    'extraction_method': 'regex'
                }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_mrp_inclusive_tax(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Check if MRP includes 'inclusive of all taxes' phrase."""
        keywords = ['inclusive of all taxes', 'inclusive of tax', 'incl. of all taxes']
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                return {
                    'value': 'Yes',
                    'confidence': 0.9,
                    'evidence_text': keyword,
                    'status': 'found',
                    'extraction_method': 'keyword_match'
                }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_consumer_care(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract consumer care contact (phone or email)."""
        phone_pattern = r'(\d{10}|\+91\s*\d{10}|1800[-\s]?\d{3}[-\s]?\d{4})'
        email_pattern = r'([\w\.-]+@[\w\.-]+\.\w+)'
        
        for result in ocr_results:
            # Try phone
            phone_match = re.search(phone_pattern, result['text'])
            if phone_match:
                return {
                    'value': phone_match.group(1),
                    'confidence': result['confidence'],
                    'evidence_text': result['text'],
                    'bbox': result['bbox'],
                    'status': 'found',
                    'extraction_method': 'regex_phone'
                }
            
            # Try email
            email_match = re.search(email_pattern, result['text'])
            if email_match:
                return {
                    'value': email_match.group(1),
                    'confidence': result['confidence'],
                    'evidence_text': result['text'],
                    'bbox': result['bbox'],
                    'status': 'found',
                    'extraction_method': 'regex_email'
                }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_country_of_origin(self, text: str, ocr_results: List[Dict]) -> Dict:
        """Extract country of origin (for imported goods)."""
        countries = ['india', 'made in india', 'product of india', 'china', 'usa', 'uk', 'germany']
        text_lower = text.lower()
        
        for country in countries:
            if country in text_lower:
                return {
                    'value': country.title(),
                    'confidence': 0.7,
                    'evidence_text': country,
                    'status': 'found',
                    'extraction_method': 'keyword_match'
                }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }
    
    def _extract_by_anchor_phrase(self, text: str, ocr_results: List[Dict], 
                                  anchor_phrases: List[str]) -> Dict:
        """Extract text near anchor phrase."""
        text_lower = text.lower()
        
        for anchor in anchor_phrases:
            if anchor in text_lower:
                # Find the text containing the anchor
                for result in ocr_results:
                    if anchor in result['text'].lower():
                        # Get the next result as manufacturer name
                        result_idx = ocr_results.index(result)
                        if result_idx + 1 < len(ocr_results):
                            next_result = ocr_results[result_idx + 1]
                            return {
                                'value': next_result['text'],
                                'confidence': (result['confidence'] + next_result['confidence']) / 2 * 0.95,
                                'evidence_text': f"{result['text']} {next_result['text']}",
                                'bbox': next_result['bbox'],
                                'status': 'found',
                                'extraction_method': 'anchor_phrase'
                            }
                        else:
                            # Just return the anchor text
                            extracted_text = result['text'].replace(anchor, '').strip()
                            return {
                                'value': extracted_text if extracted_text else result['text'],
                                'confidence': result['confidence'] * 0.9,
                                'evidence_text': result['text'],
                                'bbox': result['bbox'],
                                'status': 'found',
                                'extraction_method': 'anchor_phrase'
                            }
        
        return {
            'value': None,
            'confidence': 0.0,
            'evidence_text': '',
            'status': 'not_found',
            'extraction_method': 'none'
        }


def extract_declarations(ocr_results: List[Dict]) -> Dict[str, Any]:
    """Convenience function to extract all declarations."""
    extractor = DeclarationExtractor()
    return extractor.extract_all_fields(ocr_results)
