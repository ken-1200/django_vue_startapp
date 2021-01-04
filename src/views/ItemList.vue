<template>
  <div id="app">
    <!-- 商品一覧 -->
    <v-container fluid>

      <!-- エラー -->
      <p v-if="isErrored">{{ error }}</p>

      <v-layout wrap row>
        <v-flex cols=2 md=3 xl=4>
          <v-carousel
            :continuous="true"
            :cycle="cycle"
            :show-arrows="true"
            hide-delimiter-background
            delimiter-icon="mdi-minus"
            height="500"
          >
            <v-carousel-item
              v-for="(slide, i) in slides"
              :key="i"
            >
              <v-sheet
                :color="colors[i]"
                height="100%"
                tile
              >
                <v-row
                  class="fill-height"
                  align="center"
                  justify="center"
                >
                  <div class="display-3">
                    {{ slide }} Slide
                  </div>
                </v-row>
              </v-sheet>
            </v-carousel-item>
          </v-carousel>

          <v-card-title>Infomation</v-card-title>
          <v-card-text>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque a leo ante. Vivamus ac lacinia diam. Aenean sed magna ligula. Vivamus ultrices euismod sapien, non egestas erat semper quis. Curabitur lorem erat, finibus at fringilla ut, egestas id sapien. Suspendisse dignissim felis vitae urna ultrices varius. Integer vulputate augue scelerisque.
          </v-card-text>

          <v-card-title class="item_list">NEW KIMONO ARRIVAL</v-card-title>

          <transition-group
          name="fade"
          tag="div"
          class="row row--dense"
          >
            <v-col
              v-for="(item, index) in items"
              :key="index"
              class="d-flex child-flex"
              cols=2 md=3 xl=4
            >
              <v-card
                elevation-24
                hover
                @click.stop="itemDetail(item.pk)"
                outlined
              >
                <v-img
                  :src="item.fields.item_img"
                  class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                  aspect-ratio="1"
                >
                  <v-card-title
                    v-text="item.fields.item_name"
                  ></v-card-title>

                  <!-- <template v-slot:placeholder>
                    <v-row
                      class="fill-height ma-0"
                      align="center"
                      justify="center"
                    >
                      <v-progress-circular
                        indeterminate
                        color="grey lighten-5"
                      ></v-progress-circular>
                    </v-row>
                  </template> -->
                </v-img>

                <v-card-subtitle
                  v-text="item.fields.item_detail"
                ></v-card-subtitle>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn icon>
                    <v-icon x-small>{{ item.fields.item_price }}円</v-icon>
                  </v-btn>

                  <v-btn icon>
                    <v-icon x-small>{{ item.fields.item_total }}個</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </transition-group>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      error: null,
      colors: [
        'green',
        'secondary',
        'yellow darken-4',
        'red lighten-2',
        'orange darken-1',
      ],
      cycle: true,
      slides: [
        'First',
        'Second',
        'Third',
        'Fourth',
        'Fifth',
      ],
    }
  },
  methods: {
    itemDetail(item_id) {
      this.$router.push(`/items/${item_id}`);
    },
    isErrored() {
      return this.error != null;
    },
  },
  async created() {
    // ここは、ユーザー側、ストア側両方が見れる商品一覧
    await this.$store.dispatch('getItemList');
    this.items = this.$store.getters.allItemListData;
    this.error = this.$store.getters.error;

    // エラー表示
    if (this.items.length != 0) {
      // エラー内容表示(ex)Notfound..)
      this.error = this.$store.getters.error;
    } else {
      // 商品がない時(0個返却された)
      this.error = ' 商品がありません。';
    }
  },
}
</script>

<style lang="scss">
/* fade-move */
.fade-move {
  transition: transform 1.26s;
}
/* fade-transition */
.fade-enter, 
.fade-leave-to {
  /* 現れる時の最初の状態, 消えるときの最後の状態 */
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  /* 現れる時のトランジションの状態, 消えるときのトランジションの状態 */
  transition: opacity 1.26s;
}
.fade-enter-to,
.fade-leave {
  /* 現れる時の最後の状態, 消える時の最初の状態 */
  opacity: 1;
}

.v-btn--icon.v-size--default {
  height: 36px;
  width: 32px;
}
.v-card__subtitle {
  text-align: left;
  padding: 16px;
}
.item_list {
  justify-content: center;
  font-size: 1.7rem;
}
.v-image {
  z-index: 0;
}
</style>