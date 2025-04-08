<script lang="ts">
  export let size = 216;

  const square = size / 3;
  const double = square * 2; 
</script>

<div
  class="loading-animation"
  style="width: {size}px; height: {size}px;"
>
  <div
    class="top-left"
    style="width: {size}px; height: {size}px;"
  >
    {#each Array(9) as _, i}
      <svg
        class="square {i % 2 === 1 ? 'white' : ''}"
        style="width: {square}px; height: {square}px;"
      />
    {/each}
  </div>

  <svg
    class="square white right-top"
    style="width: {square}px; height: {square}px; right: {-square}px; top: 0;"
  />
  <svg
    class="square white right-bottom"
    style="width: {square}px; height: {square}px; right: {-square}px; top: {double}px;"
  />
  <svg
    class="square white bottom-left"
    style="width: {square}px; height: {square}px; left: 0; top: {size}px;"
  />
  <svg
    class="square white bottom-right"
    style="width: {square}px; height: {square}px; left: {double}px; top: {size}px;"
  />
</div>

<style>
  .loading-animation {
    position: relative;
  }

  .top-left {
    display: flex;
    flex-wrap: wrap;
  }

  .square {
    background-color: transparent;
  }

  .white {
    background-color: #ffffff;
  }

  .right-top,
  .right-bottom,
  .bottom-left,
  .bottom-right {
    position: absolute;
  }
</style>
