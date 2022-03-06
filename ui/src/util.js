export default {
  sleep: (seconds) =>
    new Promise((resolve) => setTimeout(resolve, seconds * 1000)),
  is_res_ok: (res) => res.status == 200,
  check_password: (password) => password === "HEALLO", // TODO: Improve logic to check password
  get_parties: (query) => (query ? [query, query, "asca", "KNASJ AKSJB"] : []), // TODO: complete implementation,
};
