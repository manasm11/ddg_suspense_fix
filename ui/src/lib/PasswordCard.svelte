<script>
  export let input_ref;
  import u from "../util";
  import { is_login } from "../stores";

  let invalid_password = false;

  function submit() {
    const is_password_correct = u.check_password(input_ref.value);
    is_login.set(is_password_correct);
    invalid_password = !is_password_correct;
  }
</script>

<form
  on:submit|preventDefault={submit}
  class="p-6 w-80 h-40 rounded-lg shadow-2xl border-gray-400 border bg-white"
>
  <h4 class="text-xl font-bold mb-4">Enter Password to proceed</h4>
  <input
    class="w-full outline-blue-800 p-3 border-2 border-slate-400 rounded-lg"
    type="password"
    placeholder="Enter password"
    bind:this={input_ref}
  />
  {#if invalid_password}
    <p class="text-red-500 text-sm">Invalid Password</p>
  {/if}
</form>
