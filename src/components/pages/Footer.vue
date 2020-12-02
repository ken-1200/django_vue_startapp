<template>
  <div id="app">
    <footer class="footer appear up">
      <div class="logo item">
        <img src="images/logo.svg" alt="" class="logo__img">
        <span class="logo__kimono">Kimono</span>
        <span class="logo__style">Style</span>
      </div>
      <nav class="footer__anav">
        <ul class="footer__ul">
          <li class="footer__li item"><router-link to="/">Service</router-link></li>
          <li class="footer__li item"><router-link to="/">Contact</router-link></li>
          <li class="footer__li item"><router-link to="/">Company</router-link></li>
          <li class="footer__li item"><router-link to="/">Sitemap</router-link></li>
        </ul>
        <div class="footer__copyright item">
          &copy; 2020 Ken
        </div>
      </nav>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style>
  
</style>