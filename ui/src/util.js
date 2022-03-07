import c from "./constants";

export default {
  sleep: (seconds) =>
    new Promise((resolve) => setTimeout(resolve, seconds * 1000)),
  is_res_ok: (res) => res.status == 200,
  check_password: (password) => password === "HEALLO", // TODO: Improve logic to check password
  get_parties: async (query) =>
    query
      ? await fetch(
          join(c.SERVER_URL, "possible-parties") + `?desc=${query}`
        ).then((res) => res.json())
      : [],
  join,
  strip,
};

function join(...args) {
  return (
    args.reduce(
      (result, currentValue) =>
        strip(result, "/") + "/" + strip(currentValue, "/")
    ) + "/"
  );
}

function strip(string, char) {
  const c = char ? char : "s";
  const pattern = `^$${c}+|${c}+$`;
  const re = new RegExp(pattern, "g");
  return string.replace(re, "");
}
