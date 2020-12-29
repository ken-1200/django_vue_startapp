<template>
  <div id="app">
    <v-footer
      dark
      padless
    >
      <v-card
        flat
        tile
        color="#ECEFF1"
      >
        <v-card-text>
          <v-btn
            v-for="icon in icons"
            :key="icon"
            class="VueBlack--text mx-4"
            icon
          >
            <v-icon size="24px">
              {{ icon }}
            </v-icon>
          </v-btn>
        </v-card-text>
  
        <v-card-text class="VueBlack--text">
          Phasellus feugiat arcu sapien, et iaculis ipsum elementum sit amet. Mauris cursus commodo interdum. Praesent ut risus eget metus luctus accumsan id ultrices nunc. Sed at orci sed massa consectetur dignissim a sit amet dui. Duis commodo vitae velit et faucibus. Morbi vehicula lacinia malesuada. Nulla placerat augue vel ipsum ultrices, cursus iaculis dui sollicitudin. Vestibulum eu ipsum vel diam elementum tempor vel ut orci. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
        </v-card-text>
  
        <v-divider></v-divider>
  
        <v-card-text class="VueBlack--text">
          {{ new Date().getFullYear() }} — <strong>&copy; Ken</strong>
        </v-card-text>
      </v-card>
    </v-footer>
  </div>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      icons: [
        'mdi-facebook',
        'mdi-twitter',
        'mdi-linkedin',
        'mdi-instagram',
      ],
    }
  }
}
</script>

<style lang="scss">
.v-application .VueBlack--text {
  color: $cVueBlack !important;
}
</style>