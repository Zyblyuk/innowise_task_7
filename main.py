from BugCatcher import BugCatcherByRule


columns_name = [
    'error_code', 'error_message',
    'severity', 'log_location',
    'mode', 'model', 'graphics',
    'session_id', 'sdkv', 'test_mode',
    'flow_id', 'flow_type', 'sdk_date',
    'publisher_id', 'game_id',
    'bundle_id', 'appv', 'language',
    'os', 'adv_id', 'gdpr',
    'ccpa', 'country_code', 'date'
]

alerts = BugCatcherByRule('csv/data.csv', columns_name)

alerts.data = alerts.data[
    (alerts.data["severity"] == "Error") &
    (alerts.data["error_code"] > 0)
    ]

alerts.anything_to_datetime('sdk_date')

alerts.send_alerts_by_rules("sdk_date", "minute", 100)
alerts.send_alerts_by_rules("sdk_date", "hour", 10, 'bundle_id', "com.pregnantcatemma.virtualpet")
alerts.send_alerts_by_rules("sdk_date", "day", 300)
