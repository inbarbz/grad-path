<template>
    <div class="star" :style="{ backgroundColor: starColor }">
        {{ score }}
    </div>
</template>

<script>
export default {
    props: {
        score: {
            type: Number,
            required: true
        }
    },
    computed: {
        starColor() {
            const greenValue = Math.floor(this.score * 2.55);
            const redValue = 255 - greenValue;
            return `rgb(${redValue}, ${greenValue}, 0)`;
        }
    }
}
</script>

<style scoped>
.star {
    display: inline-block;
    width: 50px;
    height: 50px;
    background-color: green;
    clip-path: polygon(50% 0%,
            61% 35%,
            98% 35%,
            68% 57%,
            79% 91%,
            50% 70%,
            21% 91%,
            32% 57%,
            2% 35%,
            39% 35%);
    color: white;
    text-align: center;
    line-height: 50px;
}
</style>