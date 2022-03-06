<script>
  import { server_working } from "./stores";
  import PasswordCard from "./lib/PasswordCard.svelte";
  import { onMount } from "svelte";
  let input_ref;

  onMount(() => input_ref.focus());
</script>

<main class="flex flex-col bg-slate-200 h-screen w-screen">
  {#if !$server_working}
    <div class="bg-red-500 text-white">SERVER NOT WORKING</div>
  {/if}

  <div class="self-center mt-16">
    <PasswordCard bind:input_ref />
  </div>
</main>
