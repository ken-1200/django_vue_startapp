<template>
  <div id="app">
    <!-- 商品詳細一覧 -->
    <h1>自分の商品一覧画面(権限がないと見れない)</h1>
    <p v-if="isErrored">{{ error }}</p>

    <v-layout wrap row>
      <v-flex cols=2 md=3 xl=4>
        <v-card-title class="item_list">NEW KIMONO ARRIVAL</v-card-title>

        <transition-group
          name="fade"
          tag="div"
          class="row row--dense"
        >
          <v-col
            v-for="(item, index) in detailItems"
            :key="index"
            class="d-flex child-flex"
            cols=2 md=3 xl=4
          >
            <v-card elevation-24 hover @click.stop="itemEdit(item.pk)">
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
                <v-btn icon @click.stop="itemDelete(item.pk)">
                  <v-icon x-small>削除</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </transition-group>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      detailItems: [],
      error: null,
    }
  },
  computed: {
    accessToken() {
      return this.$store.getters.access_token;
    },
    getByStoreId() {
      return this.$store.getters.store_id;
    },
    isErrored() {
      return this.error != null;
    },
  },
  methods: {
    itemEdit(item_id) {
      this.$router.push(`/item_detail/edit/${item_id}`);
    },
    async itemDelete(item_id) {
      await axios.delete(`/all/${item_id}/delete_item/`)
      .then(response => {
        Boolean(response.data.data.deleted_at);

        // リロードする
        this.$router.go({ name: 'item_detail', query: { page: this.$store.getters.store_id }});
      })
      .catch(error => {
        console.log(error);
        this.error = error;
      });
    },
  },
  // 非同期
  async created() {
    // プロミスが帰って来たら(レスポンス)表示する、またはエラー表示
    await this.$store.dispatch('getItem');
    this.detailItems = this.$store.getters.storeItemData;
    this.error = this.$store.getters.error;

    // エラー表示
    if (this.detailItems.length != 0) {
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
</style>