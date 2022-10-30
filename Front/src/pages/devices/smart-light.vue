<template>
  <v-row justify="center" align="center">
    <v-col cols="12" class="d-flex flex-column" v-if="!loading">
      <h2>Smart Light</h2>
      <span>Estado: {{ stateLight.typeLight }}</span>
      <span v-if="duration">Último tiempo de ida y vuelta: {{ duration }}</span>
      <ColorPicker :hue="color.hue" @input="onInput" @select="onSelect"></ColorPicker>
      <v-btn 
      width="120"
      @click="sendStateService('Apagar')"
      color="red">
        <v-icon>
          mdi-power
        </v-icon>
        {{ "Apagar" }}
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
  import ColorPicker from '@/lib/ColorPicker.vue';
export default {
  name: 'SmartLightPage',
  layout: 'auth',
  components: { ColorPicker },
  data(){
    return {
      color: {
        hue: 50,
        saturation: 100,
        luminosity: 50,
        alpha: 1,
        rgb: {
          r: 255,
          g: 212,
          b: 0
        },
      },
      stateLight: '',
      values: ['Rojo','Verde'],
      loading: true,
      duration: 0
    }
  },
  methods: {
    ...mapActions("smart-light",['getState', 'sendState']),
    async getStateService(){
      try {
        this.loading = true
        let res = await this.getState()
        if(res.status){
          this.stateLight = res.data
          console.log("res", res)
          if(res.data.command != 'Apagar'){
            let s = res.data.command.split(':')
            let r = Number(s[0])
            let g = Number(s[1])
            let b = Number(s[2])
            this.color.rgb = { r, g, b}
            await this.rgbToHsl(r,g,b)
          }
        }
      } catch (error) {
        console.log("error", error)
      } finally {
        this.loading = false
      }
    },
    async sendStateService(rgb){
      try {
        this.loading = true
        let res = await this.sendState(rgb)
        if(res.status){
          this.duration = res.data.duration
          await this.getStateService()
        }
      } catch (error) {
        console.log("error", error)
      } finally {
        this.loading = false
      }
    },
    onInput(value) { 
      this.color.hue = value
      let { hue, saturation, luminosity} = this.color
      this.color.rgb = this.hslToRgb(hue, saturation, luminosity)
    },
    async onSelect(value) {
      let { r, g, b } = this.color.rgb
      let rgb = `${r}:${g}:${b}`
      await this.sendStateService(rgb)
    },
    hslToRgb(h, s, l){
      let r, g, b
			if( h=="" ) h=0;
			if( s=="" ) s=0;
			if( l=="" ) l=0;
			h = parseFloat(h);
			s = parseFloat(s);
			l = parseFloat(l);
			if( h<0 ) h=0;
			if( s<0 ) s=0;
			if( l<0 ) l=0;
			if( h>=360 ) h=359;
			if( s>100 ) s=100;
			if( l>100 ) l=100;
			s/=100;
			l/=100;
			let C = (1-Math.abs(2*l-1))*s;
			let hh = h/60;
			let X = C*(1-Math.abs(hh%2-1));
			r = g = b = 0;
			if( hh>=0 && hh<1 )
			{
				r = C;
				g = X;
			}
			else if( hh>=1 && hh<2 )
			{
				r = X;
				g = C;
			}
			else if( hh>=2 && hh<3 )
			{
				g = C;
				b = X;
			}
			else if( hh>=3 && hh<4 )
			{
				g = X;
				b = C;
			}
			else if( hh>=4 && hh<5 )
			{
				r = X;
				b = C;
			}
			else
			{
				r = C;
				b = X;
			}
			let m = l-C/2;
			r += m;
			g += m;
			b += m;
			r *= 255.0;
			g *= 255.0;
			b *= 255.0;
			r = Math.round(r);
			g = Math.round(g);
			b = Math.round(b);
			let hex = r*65536+g*256+b;
			hex = hex.toString(16,6);
			let len = hex.length;
			if( len<6 )
				for(let i=0; i<6-len; i++)
					hex = '0'+hex;
      return {r,g,b}
    },
    rgbToHsl(r, g, b){      
      let h, s, l
      if( r=="" ) r=0;
      if( g=="" ) g=0;
      if( b=="" ) b=0;
      r = parseFloat(r);
      g = parseFloat(g);
      b = parseFloat(b);
      if( r<0 ) r=0;
      if( g<0 ) g=0;
      if( b<0 ) b=0;
      if( r>255 ) r=255;
      if( g>255 ) g=255;
      if( b>255 ) b=255;
      let hex = r*65536+g*256+b;
      hex = hex.toString(16,6);
      let len = hex.length;
      if( len<6 )
        for(let i=0; i<6-len; i++)
          hex = '0'+hex;
      r/=255;
      g/=255;
      b/=255;
      let M = Math.max(r,g,b);
      let m = Math.min(r,g,b);
      let d = M-m;
      if( d==0 ) h=0;
      else if( M==r ) h=((g-b)/d)%6;
      else if( M==g ) h=(b-r)/d+2;
      else h=(r-g)/d+4;
      h*=60;
      if( h<0 ) h+=360;
      l = (M+m)/2;
      if( d==0 )
        s = 0;
      else
        s = d/(1-Math.abs(2*l-1));
      s*=100;
      l*=100;
      this.color.hue = h
    }
  },
  async mounted() {
    await this.getStateService()
  }
}
</script>
