-- Digital Loan Application Process Improvement | SQL analysis (SQLite syntax)
-- Table: loan_applications (loaded from data/loan_applications.csv)

-- name: q1_overall_kpis
SELECT COUNT(*) AS total_applications,
       SUM(final_status = 'Approved') AS approved,
       SUM(final_status = 'Rejected') AS rejected,
       SUM(final_status = 'Abandoned') AS abandoned,
       ROUND(100.0 * SUM(final_status = 'Approved') / COUNT(*), 1) AS approval_rate_pct,
       ROUND(100.0 * SUM(final_status = 'Abandoned') / COUNT(*), 1) AS abandonment_rate_pct,
       ROUND(AVG(days_to_decision), 1) AS avg_days_to_decision
FROM loan_applications;

-- name: q2_funnel
SELECT '1. Application Started' AS stage, COUNT(*) AS applications FROM loan_applications
UNION ALL SELECT '2. Personal Details', SUM(furthest_stage >= 2) FROM loan_applications
UNION ALL SELECT '3. Document Upload', SUM(furthest_stage >= 3) FROM loan_applications
UNION ALL SELECT '4. Verification', SUM(furthest_stage >= 4) FROM loan_applications
UNION ALL SELECT '5. Credit Assessment', SUM(furthest_stage >= 5) FROM loan_applications
UNION ALL SELECT '6. Decision', SUM(furthest_stage >= 6) FROM loan_applications;

-- name: q3_abandonment_by_stage
SELECT drop_stage, COUNT(*) AS abandoned_applications,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM loan_applications WHERE final_status = 'Abandoned'), 1) AS pct_of_all_abandonments
FROM loan_applications WHERE final_status = 'Abandoned'
GROUP BY drop_stage ORDER BY abandoned_applications DESC;

-- name: q4_channel_performance
SELECT channel, COUNT(*) AS applications,
       ROUND(100.0 * SUM(final_status = 'Abandoned') / COUNT(*), 1) AS abandonment_rate_pct,
       ROUND(100.0 * SUM(final_status = 'Approved') / COUNT(*), 1) AS approval_rate_pct,
       ROUND(AVG(days_to_decision), 1) AS avg_days_to_decision,
       ROUND(100.0 * AVG(docs_complete_first_attempt), 1) AS docs_complete_first_attempt_pct
FROM loan_applications GROUP BY channel ORDER BY abandonment_rate_pct DESC;

-- name: q5_document_completeness_impact
SELECT CASE docs_complete_first_attempt WHEN 1 THEN 'Complete on first attempt' ELSE 'Incomplete / needs resubmission' END AS document_status,
       COUNT(*) AS applications,
       ROUND(100.0 * SUM(final_status = 'Abandoned') / COUNT(*), 1) AS abandonment_rate_pct,
       ROUND(100.0 * SUM(final_status = 'Approved') / COUNT(*), 1) AS approval_rate_pct,
       ROUND(AVG(days_to_decision), 1) AS avg_days_to_decision
FROM loan_applications GROUP BY docs_complete_first_attempt;

-- name: q6_processing_time_by_employment
SELECT employment_type, COUNT(*) AS decided_applications,
       ROUND(AVG(verification_days), 1) AS avg_verification_days,
       ROUND(AVG(days_to_decision), 1) AS avg_days_to_decision
FROM loan_applications WHERE final_status IN ('Approved','Rejected')
GROUP BY employment_type ORDER BY avg_days_to_decision DESC;

-- name: q7_verification_wait_vs_abandonment
SELECT CASE WHEN verification_days = 0 THEN 'Not reached'
            WHEN verification_days <= 4 THEN '1-4 days'
            WHEN verification_days <= 7 THEN '5-7 days'
            ELSE '8+ days' END AS verification_wait,
       COUNT(*) AS applications,
       ROUND(100.0 * SUM(drop_stage = 'Verification') / COUNT(*), 1) AS abandoned_at_verification_pct
FROM loan_applications WHERE furthest_stage >= 4
GROUP BY verification_wait ORDER BY MIN(verification_days);

-- name: q8_rejection_reasons
SELECT rejection_reason, COUNT(*) AS rejected_applications,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM loan_applications WHERE final_status = 'Rejected'), 1) AS pct_of_rejections
FROM loan_applications WHERE final_status = 'Rejected'
GROUP BY rejection_reason ORDER BY rejected_applications DESC;

-- name: q9_monthly_trend
SELECT SUBSTR(application_date, 1, 7) AS month, COUNT(*) AS applications,
       ROUND(100.0 * SUM(final_status = 'Approved') / COUNT(*), 1) AS approval_rate_pct,
       ROUND(100.0 * SUM(final_status = 'Abandoned') / COUNT(*), 1) AS abandonment_rate_pct
FROM loan_applications GROUP BY month ORDER BY month;

-- name: q10_value_lost_to_abandonment
SELECT ROUND(SUM(CASE WHEN final_status = 'Abandoned' THEN loan_amount END) / 1000000.0, 1) AS abandoned_loan_value_millions,
       ROUND(SUM(CASE WHEN final_status = 'Abandoned' AND drop_stage = 'Document Upload' THEN loan_amount END) / 1000000.0, 1) AS lost_at_document_upload_millions,
       ROUND(SUM(CASE WHEN final_status = 'Approved' THEN loan_amount END) / 1000000.0, 1) AS approved_loan_value_millions
FROM loan_applications;
