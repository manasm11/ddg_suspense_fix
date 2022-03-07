<script>
  import { server_working, is_login } from "./stores";
  import SingleInputCard from "./lib/SingleInputCard.svelte";
  import PartyList from "./lib/PartyList.svelte";
  let possible_parties;
</script>

<main class="flex flex-col bg-slate-200 h-screen w-screen">
  {#if !$server_working}
    <div class="bg-red-500 text-white">SERVER NOT WORKING</div>
  {/if}

  <div class="self-center mt-16">
    {#if !$is_login}
      <SingleInputCard type="password" />
    {:else}
      <SingleInputCard type="desc" bind:possible_parties />
    {/if}
  </div>

  <PartyList parties={possible_parties} />
</main>
