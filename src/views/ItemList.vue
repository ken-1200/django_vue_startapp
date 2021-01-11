<template>
  <div id="app">
    <!-- 商品一覧 -->
    <v-container fluid>

      <v-layout wrap row>
        <v-flex cols=12 md=3 xl=4>
          <v-carousel
            :continuous="true"
            :cycle="cycle"
            :show-arrows="true"
            hide-delimiter-background
            delimiter-icon="mdi-minus"
            height="800"
          >
            <v-carousel-item
              v-for="(slide, i) in slides"
              :key="i"
              :src="slide.src"
            >
            </v-carousel-item>
          </v-carousel>

          <v-card outlined color="#f4f7fa">
            <v-card-title id="titleInfo">Infomation</v-card-title>
            <v-card-text>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque a leo ante. Vivamus ac lacinia diam. Aenean sed magna ligula. Vivamus ultrices euismod sapien, non egestas erat semper quis. Curabitur lorem erat, finibus at fringilla ut, egestas id sapien. Suspendisse dignissim felis vitae urna ultrices varius. Integer vulputate augue scelerisque.
            </v-card-text>

            <v-card-title class="item_list">NEW FURISODE ARRIVAL</v-card-title>
          </v-card>

          <!-- エラー -->
          <template v-if="isErrored">{{ error }}</template>

          <transition-group
            name="fade"
            tag="div"
            class="row row--dense"
          >
            <v-col
              v-for="(item, index) in items"
              :key="index"
              class="d-flex child-flex"
              cols=12 md=3 xl=4
            >
              <v-card
                @click.stop="itemDetail(item.pk)"
                elevation-24
                hover
                outlined
              >
                <v-img
                  :src="item.fields.item_img"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                  aspect-ratio="1"
                  height="200px"
                >

                  <!-- プログレス -->
                  <template v-slot:placeholder>
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
                  </template>
                </v-img>

                <!-- タイトル/サブタイトル -->
                <v-card-title
                  v-text="item.fields.item_name"
                ></v-card-title>
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
        {
          src: require('../../public/image/sample1.jpg'),
        },
        {
          src: require('../../public/image/sample2.jpg'),
        },
        {
          src: require('../../public/image/sample3.jpg'),
        },
        {
          src: require('../../public/image/sample4.jpg'),
        },
        {
          src: require('../../public/image/sample5.jpg'),
        },
        {
          src: require('../../public/image/sample6.jpg'),
        },
      ],
    }
  },
  methods: {
    itemDetail(item_id) {
      this.$router.push(`/items/${item_id}`);
    },
  },
  computed: {
    isErrored() {
      return this.error != null;
    },
  },
  async created() {
    // ここは、ユーザー側、ストア側両方が見れる商品一覧
    await this.$store.dispatch('getItemList');
    this.items = this.$store.getters.allItemListData;

    this.items.forEach(el => {
      // 商品詳細を格納
      const text = el.fields.item_detail;
      
      if (!(text.length <= 100)) {
        // 75文字以上の文章は75字以降に...をつける
        el.fields.item_detail = text.substring(0, 74) + "...";
      }

      // 画像がないものはこっち
      if (el.fields.item_img == "") {
        el.fields.item_img = "http://localhost:8001/media/image/sample_image.jpg";
      } else {
        // 画像あり
        el.fields.item_img = "http://localhost:8001/media/" + el.fields.item_img;
      }
    });

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

<style lang="scss" scoped>
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
.v-card {
  &__title {
    align-items: center;
    text-align: left;
    display: flex;
    flex-wrap: wrap;
    font-size: .701rem;
    font-weight: 500;
    letter-spacing: .0125em;
    line-height: 2rem;
    word-break: break-all;
  }

  &__subtitle {
    text-align: left;
    padding: 16px;
    font-size: .669rem;
    font-weight: 400;
    line-height: 1.375rem;
    letter-spacing: .0071428571em;
  }
}
#titleInfo {
  font-size: 1.25rem;
}
.item_list {
  justify-content: center;
  font-size: 1.7rem;
}
.v-image {
  z-index: 0;
}
</style>