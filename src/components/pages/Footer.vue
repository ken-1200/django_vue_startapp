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
            v-for="(icon, i) in icons"
            :key="i"
            class="VueBlack--text mx-4"
            icon
            @click.stop="clickIcon(i)"
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
        'mdi-home',
        'mdi-facebook',
        'mdi-twitter',
        'mdi-instagram',
      ],
    }
  },
  methods: {
    clickIcon(index) {
      switch (index) {
        case 0:
          this.$router.push('/item_list');
          break;
        case 1:
          window.open("https://www.facebook.com/profile.php?id=100049334573408", '_blank', 'width=1024,height=768,scrollbars=yes,resizable=yes');
          break;
        case 2:
          window.open("https://twitter.com", '_blank', 'width=1024,height=768,scrollbars=yes,resizable=yes');
          break;
        case 3:
          window.open("https://www.instagram.com/macd_a1200/?hl=ja", '_blank', 'width=1024,height=768,scrollbars=yes,resizable=yes');
          break;
        default:
          this.$router.push('/');
      }
    },
  }
}
</script>

<style lang="scss">
.v-application .VueBlack--text {
  color: $cVueBlack !important;
}
</style>