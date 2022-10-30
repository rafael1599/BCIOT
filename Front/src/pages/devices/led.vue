<template>
    <v-row justify="center" align="center">
      <v-col cols="12" class="d-flex flex-column" v-if="!loading">
        <h2>LED</h2>
        <span>Estado: {{ stateLight.typeLight }}</span>
        <span v-if="duration">Último tiempo de ida y vuelta: {{ duration }}</span>
        <v-btn 
        width="120"
        @click="sendStateService()"
        :color="nextLight.color">
          <v-icon>
            mdi-power
          </v-icon>
          {{ nextLight.text }}
        </v-btn>
      </v-col>
      <v-col cols="12" class="d-flex flex-column" v-else>
        <v-progress-circular
          indeterminate
        ></v-progress-circular>
      </v-col>
    </v-row>
</template>
  
<script>
import { mapActions } from 'vuex'
export default {
    name: 'LEDPage',
    layout: 'auth',
    data(){
      return {
        stateLight: {
          command: 'Encender',
          typeLight: ''
        },
        values: ['Apagar','Encender'],
        loading: true,
        duration: 0
      }
    },
    methods: {
      ...mapActions("led",['getState', 'sendState']),
      async getStateService(){
        try {
          this.loading = true
          let res = await this.getState()
          if(res.status){
            this.stateLight = res.data
          }
        } catch (error) {
          console.log("error", error)
        } finally {
          this.loading = false
        }
      },
      async sendStateService(){
        try {
          this.loading = true
          let res = await this.sendState(this.negativeValue)
          if(res.status){
            this.duration = res.data.duration
            await this.getStateService()
          }
        } catch (error) {
          console.log("error", error)
        } finally {
          this.loading = false
        }
      }
    },
    computed: {
      negativeValue(){
        return this.values.filter(x => x != this.stateLight.command)[0]
      },
      nextLight(){
        if(this.stateLight.command == 'Apagar'){
          return {
            text: 'Encender',
            color: 'green' //00000000000
          }
        }
        return {
          text: 'Apagar', //000000
          color: 'red'
        }
      }
    },
    async mounted() {
      await this.getStateService()
    }
}
</script>
  