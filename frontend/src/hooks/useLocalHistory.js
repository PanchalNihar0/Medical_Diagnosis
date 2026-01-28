import { useState, useEffect } from 'react'

const STORAGE_KEY = 'mediscreen_history'
const MAX_HISTORY = 50

/**
 * Hook for managing local prediction history in localStorage.
 */
export function useLocalHistory() {
    const [history, setHistory] = useState([])

    // Load history from localStorage on mount
    useEffect(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY)
            if (stored) {
                setHistory(JSON.parse(stored))
            }
        } catch (err) {
            console.error('Failed to load history:', err)
        }
    }, [])

    // Save to localStorage whenever history changes
    const saveHistory = (newHistory) => {
        setHistory(newHistory)
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(newHistory))
        } catch (err) {
            console.error('Failed to save history:', err)
        }
    }

    /**
     * Add a new prediction to history.
     */
    const addToHistory = (disease, inputs, result) => {
        const entry = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            disease,
            inputs,
            prediction: result.result.prediction,
            probability: result.result.probability,
            confidenceLevel: result.result.confidence_level,
        }

        const newHistory = [entry, ...history].slice(0, MAX_HISTORY)
        saveHistory(newHistory)

        return entry
    }

    /**
     * Get history for a specific disease.
     */
    const getHistoryByDisease = (disease) => {
        return history.filter(h => h.disease === disease)
    }

    /**
     * Clear all history.
     */
    const clearHistory = () => {
        saveHistory([])
    }

    /**
     * Clear history for a specific disease.
     */
    const clearDiseaseHistory = (disease) => {
        const newHistory = history.filter(h => h.disease !== disease)
        saveHistory(newHistory)
    }

    /**
     * Delete a specific entry.
     */
    const deleteEntry = (id) => {
        const newHistory = history.filter(h => h.id !== id)
        saveHistory(newHistory)
    }

    return {
        history,
        addToHistory,
        getHistoryByDisease,
        clearHistory,
        clearDiseaseHistory,
        deleteEntry,
    }
}

export default useLocalHistory
