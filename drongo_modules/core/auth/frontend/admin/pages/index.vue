<template>
  <div class="page">
    <h2 class="page__title">
      <i class="icon-lock"></i>
      Auth
    </h2>

    <div class="panel">
      <div class="panel__head">
        Quick Links
      </div>
      <div class="panel__body">
        <nuxt-link class="button button--primary" to="/auth/users"><i class="icon-user"></i> Users</nuxt-link>
        &nbsp;
        <nuxt-link class="button button--primary" to="/auth/groups"><i class="icon-people"></i> Groups</nuxt-link>
        &nbsp;
        <nuxt-link class="button button--primary" to="/auth/permissions"><i class="icon-key"></i> Permissions</nuxt-link>
      </div>
    </div>
  </div>
</template>
