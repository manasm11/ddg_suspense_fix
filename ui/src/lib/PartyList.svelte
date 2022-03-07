<script>
  export let parties;
  let copied = false;
  let _timeout;

  function copy(party) {
    return async () => {
      clearTimeout(_timeout);
      await navigator.clipboard.writeText(party);
      copied = party;
      _timeout = setTimeout(() => (copied = ""), 3000);
    };
  }
</script>

{#if parties && parties.length}
  <div
    class="bg-white flex flex-col w-1/2 self-center mt-3 border-2 border-blue-700"
  >
    {#each parties as party}
      <div class="flex justify-between p-4">
        <div class="text-lg">
          {party}
        </div>
        <button
          class="right-0 hover:bg-slate-200 p-2 rounded-lg active:bg-blue-300 text-xs font-semibold"
          on:click={copy(party)}
        >
          {copied == party ? "COPIED!" : "COPY"}
        </button>
      </div>
      <hr class="bg-gray-300 w-full h-0.5" />
    {/each}
  </div>
{:else if parties !== undefined && !parties.length}
  <div class="bg-red-500 text-white">NO PARTY FOUND</div>
{/if}
