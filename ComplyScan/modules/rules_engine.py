"""
ComplyScan Rule Engine Module
Evaluates extracted declarations against Legal Metrology compliance rules.
"""

from typing import Dict, List, Any
from modules.config import (
    COMPLIANCE_RULES, VERDICT_COMPLIANT, VERDICT_NON_COMPLIANT, 
    VERDICT_NEEDS_REVIEW, HIGH_CONFIDENCE, MEDIUM_CONFIDENCE, LOW_CONFIDENCE
)

class ComplianceRuleEngine:
    """Evaluates compliance based on extracted fields."""
    
    def evaluate_scan(self, extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate all extracted fields against compliance rules.
        
        Args:
            extracted_fields (dict): Fields extracted by DeclarationExtractor
        
        Returns:
            dict: Comprehensive evaluation with verdict, violations, and explanations
        """
        rule_results = []
        violations = []
        confidence_scores = []
        
        # Evaluate each rule
        for rule_id, rule_config in COMPLIANCE_RULES.items():
            field_name = rule_config['field']
            field_data = extracted_fields.get(field_name, {})
            
            result = self._evaluate_rule(rule_id, rule_config, field_data)
            rule_results.append(result)
            
            # Track violations
            if result['status'] == 'FAIL':
                violations.append({
                    'rule_id': rule_id,
                    'field': field_name,
                    'description': rule_config['description'],
                    'legal_reference': rule_config['legal_reference'],
                    'explanation': result['explanation'],
                    'severity': 'HIGH' if rule_config.get('required') else 'MEDIUM'
                })
            
            # Track confidence
            if field_data.get('confidence') is not None:
                confidence_scores.append(field_data['confidence'])
        
        # Calculate overall verdict
        verdict = self._calculate_verdict(rule_results)
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # Calculate compliance score (percentage of rules passed)
        passed_rules = sum(1 for r in rule_results if r['status'] == 'PASS')
        total_rules = len(rule_results)
        compliance_score = (passed_rules / total_rules * 100) if total_rules > 0 else 0
        
        return {
            'verdict': verdict,
            'compliance_score': compliance_score,
            'overall_confidence': overall_confidence,
            'rule_results': rule_results,
            'violations': violations,
            'total_rules_checked': total_rules,
            'rules_passed': passed_rules,
            'rules_failed': len([r for r in rule_results if r['status'] == 'FAIL']),
            'rules_review': len([r for r in rule_results if r['status'] == 'REVIEW'])
        }
    
    def _evaluate_rule(self, rule_id: str, rule_config: Dict, field_data: Dict) -> Dict:
        """Evaluate a single rule against field data."""
        field_name = rule_config['field']
        field_value = field_data.get('value')
        field_confidence = field_data.get('confidence', 0.0)
        
        # Check if field is required and missing
        if rule_config.get('required', False) and field_value is None:
            if field_confidence < MEDIUM_CONFIDENCE:
                status = 'REVIEW'
                explanation = f"Could not confidently detect required field: {field_name}"
            else:
                status = 'FAIL'
                explanation = f"Required field missing: {field_name} ({rule_config['description']})"
        
        # Field found
        elif field_value is not None:
            if field_confidence >= HIGH_CONFIDENCE:
                status = 'PASS'
                explanation = f"✓ {field_name} detected with high confidence"
            elif field_confidence >= MEDIUM_CONFIDENCE:
                status = 'PASS'  # More lenient - accept MEDIUM confidence
                explanation = f"✓ {field_name} detected (confidence: {field_confidence:.0%})"
            else:
                status = 'REVIEW'
                explanation = f"Low confidence reading for {field_name} (confidence: {field_confidence:.0%})"
        
        # Optional field not found
        else:
            if not rule_config.get('required', False):
                status = 'PASS'
                explanation = f"Optional field not required: {field_name}"
            else:
                status = 'REVIEW'
                explanation = f"Could not detect required field: {field_name}"
        
        return {
            'rule_id': rule_id,
            'field': field_name,
            'description': rule_config['description'],
            'legal_reference': rule_config.get('legal_reference', 'N/A'),
            'status': status,
            'detected_value': field_value,
            'confidence': field_confidence,
            'explanation': explanation,
            'evidence_text': field_data.get('evidence_text', '')
        }
    
    def _calculate_verdict(self, rule_results: List[Dict]) -> str:
        """
        Calculate overall verdict based on rule results.
        
        Logic:
        - NON-COMPLIANT: At least one FAIL with high confidence
        - NEEDS REVIEW: Any REVIEW status, or low confidence on FAILs
        - COMPLIANT: All rules PASS with adequate confidence
        """
        # Check for confident FAILs
        confident_fails = [r for r in rule_results if r['status'] == 'FAIL' and r['confidence'] >= MEDIUM_CONFIDENCE]
        if confident_fails:
            return VERDICT_NON_COMPLIANT
        
        # Check for any REVIEW status
        reviews = [r for r in rule_results if r['status'] == 'REVIEW']
        if reviews:
            return VERDICT_NEEDS_REVIEW
        
        # All checks passed
        return VERDICT_COMPLIANT


def evaluate_compliance(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to evaluate compliance."""
    engine = ComplianceRuleEngine()
    return engine.evaluate_scan(extracted_fields)
