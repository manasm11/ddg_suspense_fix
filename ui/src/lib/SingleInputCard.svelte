<script>
  export let type;
  export let possible_parties = [];
  import u from "../util";
  import c from "../constants";
  import { is_login } from "../stores";
  import { onMount } from "svelte";
  $: cardDetails = c.SINGLE_INPUT_CARD_DETAILS[type];

  let input_ref
  let invalid_password = false;

  onMount(() => input_ref.focus());

  function submit(type) {
    function _common() {
      input_ref.value = "";
    }
    if (type === "password") {
      return () => {
        const is_password_correct = u.check_password(input_ref.value);
        is_login.set(is_password_correct);
        invalid_password = !is_password_correct;
        _common();
      };
    }
    if (type === "desc") {
      return () => {
        possible_parties = u.get_parties(input_ref.value);
        _common();
      };
    }
  }
</script>

<form
  on:submit|preventDefault={submit(type)}
  class="flex flex-col p-6 w-80 min-h-40 rounded-lg shadow-2xl border-gray-400 border bg-white"
>
  <h4 class="text-xl font-bold mb-4">{cardDetails.heading}</h4>
  <input
    class="w-full outline-blue-800 p-3 border-2 border-slate-400 rounded-lg"
    type={cardDetails.input_type}
    placeholder={cardDetails.placeholder}
    bind:this={input_ref}
  />
  {#if invalid_password}
    <p class="text-red-500 text-sm">Invalid Password</p>
  {/if}
  <button class="bg-blue-500 text-white p-2 hover:bg-blue-600 md:hidden rounded-lg mt-3" type="submit">Submit</button>
</form>
