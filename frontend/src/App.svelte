<script>
  import { onMount } from 'svelte';
  let url = '';
  let shortUrl = '';
  let urls = [];
  let error = '';

  const API_BASE = 'http://127.0.0.1:5000';

  // Fetch all shortened URLs 
  async function fetchUrls() {
    try {
      const res = await fetch(`${API_BASE}/shorten/all`);
      urls = await res.json();
    } catch (err) {
      error = 'Failed to load URLs';
    }
  }

  // Create a Short URL
  async function shortenUrl() {
    if (!url) {
      error = 'Enter a valid URL!';
      return;
    }

    const response = await fetch(`${API_BASE}/shorten`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (response.ok) {
      const data = await response.json();
      shortUrl = `${window.location.origin}/shorten/${data.shortCode}`;
      fetchUrls();
    } else {
      error = 'Failed to create short URL!';
    }
  }

  // Retrieve Original URL
  async function getOriginalUrl(shortCode) {
    try {
      const res = await fetch(`${API_BASE}/shorten/${shortCode}`);
      const data = await res.json();
      window.open(data.url, '_blank');
    } catch (err) {
      error = 'URL not found!';
    }
  }

  // Delete Short URL
  async function deleteUrl(shortCode) {
    try {
    const response = await fetch(`${API_BASE}/shorten/${shortCode}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      fetchUrls(); // Refresh the list after deletion
    } else {
      console.error("Failed to delete URL");
    }
    } catch (err) {
      console.error("Error deleting URL:", err);
    }
  }

  // Update Short URL
  async function updateUrl(shortCode) {
    
  }
  // Fetch URLs on page load
  onMount(fetchUrls);
</script>


<h1>🔗 URL Shortener Service</h1>

<input type="text" bind:value={url} placeholder="Enter URL..." />
<button on:click={shortenUrl}>Shorten</button>

{#if shortUrl}
  <p>Short URL: <a class="short-url" href={shortUrl} target="_blank">{shortUrl}</a></p>
{/if}

{#if error}
  <p style="color: red;">{error}</p>
{/if}

<h2>📜 Shortened URLs</h2>

<table>
  <thead>
    <tr>
      <th>Short Code</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {#each urls as { shortCode}}
      <tr>
        <td>{shortCode}</td>
        <td>
          <button on:click={() => getOriginalUrl(shortCode)}>🔗 Retrieve Original URL</button>
          <button on:click={() => deleteUrl(shortCode)}>🗑️ Delete</button>
          <button on:click={() => updateUrl(shortCode)}>✏️ Update</button>
          <button on:click={() => viewStats(shortCode)}>📊 View Stats</button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: center;
  }
  th {
    background-color: #f4f4f4;
  }
  button {
    margin: 2px;
    padding: 5px 10px;
    cursor: pointer;
  }
  .short-url {
    color: blue;
    cursor: pointer;
  }
  body { font-family: Arial, sans-serif; text-align: center; }
  input, button { margin: 10px; padding: 10px; font-size: 1rem; }
  .url-list { margin-top: 20px; }
  .short-url { color: blue; cursor: pointer; }
</style>

