exports.handler = async (event, context) => {
    // Handle CORS preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            },
            body: '',
        };
    }

    try {
        // Get the API URL from query parameters
        const apiUrl = event.queryStringParameters?.url || 'https://api.data.gov.in/resource/0b344af7-b389-4e37-bf49-b4f1e59bbc49';
        const apiKey = event.queryStringParameters?.api_key || '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b';
        const format = event.queryStringParameters?.format || 'json';
        const limit = event.queryStringParameters?.limit || '1000';

        // Construct the full API URL
        const fullUrl = `${apiUrl}?api-key=${apiKey}&format=${format}&limit=${limit}`;

        // Make the API request
        const response = await fetch(fullUrl);
        const data = await response.text();

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': response.headers.get('content-type') || 'application/json',
            },
            body: data,
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ error: 'Failed to fetch data' }),
        };
    }
};
