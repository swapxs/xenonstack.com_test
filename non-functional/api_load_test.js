import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '10s', target: 20 },
        { duration: '20s', target: 50 },
        { duration: '30s', target: 100 },
        { duration: '30s', target: 200 },
        { duration: '20s', target: 100 },
        { duration: '10s', target: 50 },
    ],
};

export default () => {
    let url = 'https://api.hsforms.com/submissions/v3/integration/submit/8161231/22ff0c52-d126-484e-a693-64f0a2082746';

    let payload = JSON.stringify({
        "fields": [
            { "name": "firstname", "value": "Jhone" },
            { "name": "lastname", "value": "Doe" },
            { "name": "email", "value": "jd@gmail.com" },
            { "name": "company", "value": "XS" },
            { "name": "phone", "value": "09291233456" },
            { "name": "industry_belongs_to_", "value": "Games and Sports" },
            { "name": "in_which_agentic_platform_and_accelerator__you_are_interested_", "value": "Nexastack – Build and Managed Compound AI Stack" },
            { "name": "at_what_stage_does_your_business_belong_to_", "value": "Scale Startup" },
            { "name": "what_is_your_primary_focus_areas_", "value": "Data and Analytics" },
            { "name": "at_what_stage_is_your_ai_use_case_currently_in_", "value": "Conceptualized: Use case defined, PoC pending" },
            { "name": "what_are_the_primary_challenges_in_adopting_ai_", "value": "Data Privacy and Compliance" },
            { "name": "what_kind_of_infrastructure_does_your_organization_currently_using_", "value": "GCP" },
            { "name": "are_you_using_any_data_platform_", "value": "Microsoft Fabric" },
            { "name": "preferred_approach_for_ai_transformation", "value": "Collaborative Intelligence Agents as AI Teammates" },
            { "name": "in_which_domain_your_solution_organization_belongs_to_in_terms_of_data_privacy__trustworthy_ai", "value": "Highly Regulated Industry (Healthcare, Financials etc)" }
        ],
        "skipValidation": true,
        "legalConsentOptions": {
            "consent": {
                "consentToProcess": true,
                "text": "I agree to allow Example Company to store and process my personal data.",
                "communications": [
                    { "value": true, "subscriptionTypeId": 999, "text": "I agree to receive marketing communications from Example Company." }
                ]
            }
        },
        "context": {
            "pageUri": "https://www.xenonstack.com/",
            "pageName": "Xenonstack"
        }
    });

    let params = {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.xenonstack.com/',
            'Connection': 'keep-alive'
        },
        timeout: '10s',
    };

    let maxRetries = 3;
    let success = false;
    let res = null;

    while (maxRetries > 0 && !success) {
        try {
            res = http.post(url, payload, params);

            if (res && res.status === 200) {
                success = true;
                // console.log(`Success on try ${4 - maxRetries}, Status: ${res.status}`);
            } else {
                // console.warn(`Retrying API request (${4 - maxRetries}), Status: ${res ? res.status : 'No response'}`);
                sleep(1);
            }
        } catch (error) {
            console.error(`Error occurred: ${error}`);
        }
        maxRetries--;
    }

    if (res) {
        // console.log(`Response Body: ${res.body}`);
        check(res, {
            'API Load Test: Status is 200': (r) => r.status === 200,
            'API Load Test: Response time < 2s': (r) => r.timings.duration < 2000,
        });
    } else {
        console.error("API request failed completely after retries, no response received.");
    }

    sleep(1);
}
