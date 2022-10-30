import LEDService from '@/services/LED.service.js'
export const state = () => ({
    
})

export const getters = {}

export const mutations = {}

export const actions = {
    async getState({state, commit}){
        return await LEDService.getState(this.$axios)
    },
    async sendState({state, commit}, data){
        return await LEDService.sendState(this.$axios, data)
    },
}