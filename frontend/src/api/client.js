/**
 * API client for the Medical Diagnosis backend.
 */

const API_BASE = 'http://localhost:8000/api/v1'

/**
 * Make API request with error handling.
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`

    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        })

        if (!response.ok) {
            const error = await response.json().catch(() => ({}))
            throw new Error(error.detail || `API Error: ${response.status}`)
        }

        return response.json()
    } catch (error) {
        console.error('API Request failed:', error)
        throw error
    }
}

/**
 * Diabetes API endpoints
 */
export const diabetesApi = {
    predict: (data) => apiRequest('/diabetes/predict', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    whatIf: (data) => apiRequest('/diabetes/what-if', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    getInfo: () => apiRequest('/diabetes/info'),
}

/**
 * Heart disease API endpoints
 */
export const heartApi = {
    predict: (data) => apiRequest('/heart/predict', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    getInfo: () => apiRequest('/heart/info'),
}

/**
 * Kidney disease API endpoints
 */
export const kidneyApi = {
    predict: (data) => apiRequest('/kidney/predict', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    getInfo: () => apiRequest('/kidney/info'),
}

/**
 * Liver disease API endpoints
 */
export const liverApi = {
    predict: (data) => apiRequest('/liver/predict', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    getInfo: () => apiRequest('/liver/info'),
}

/**
 * Breast cancer API endpoints
 */
export const breastCancerApi = {
    predict: (data) => apiRequest('/breast-cancer/predict', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    getInfo: () => apiRequest('/breast-cancer/info'),
}

/**
 * Health check
 */
export const healthApi = {
    check: () => apiRequest('/health'),
}

/**
 * PDF Report generation
 */
export const reportApi = {
    generate: async (data) => {
        const response = await fetch(`${API_BASE}/report/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            throw new Error('Failed to generate report')
        }

        // Return blob for download
        return response.blob()
    },
}

export default {
    diabetes: diabetesApi,
    heart: heartApi,
    kidney: kidneyApi,
    liver: liverApi,
    breastCancer: breastCancerApi,
    health: healthApi,
    report: reportApi,
}
