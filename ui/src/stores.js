import { readable, writable } from "svelte/store";
import u from "./util";
import c from "./constants";

export const server_working = readable(false, function start(set) {
  let res = {};
  const interval = setInterval(async () => {
    try {
      res = await fetch(c.SERVER_URL);
      set(u.is_res_ok(res));
    } catch (e) {
      console.log(e);
      set(false);
    }
  }, c.SERVER_CHECK_INTERVAL_SECONDS * 1000);
  return function stop() {
    clearInterval(interval);
  };
});

export const is_login = writable(false);
