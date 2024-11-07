/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const res = await fetch(`http://127.0.0.1:7777/api/layer/available`);
    const item = await res.json();

    return { item };
}