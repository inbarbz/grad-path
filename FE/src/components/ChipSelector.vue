<template>
    <div class="p-grid">
        <div class="p-col-12" v-for="chip in   chipEntries  " :key="chip.name">
            <ToggleButton :checked="chip.selected" :onLabel="chip.name" :offLabel="chip.name"
                :class="{ 'p-highlight': chip.selected }" @change="toggleChipSelection(chip.name)" />
        </div>
    </div>
</template>

<style scoped>
/* Basic styling, you might want to use PrimeFlex for advanced layouts */
.p-grid {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
    padding-left: 2px;
    padding-right: 2px;

}

.p-highlight {
    background-color: var(--primary-color) !important;
    color: var(--primary-color-text) !important;
}
</style>

<script setup>
import ToggleButton from 'primevue/togglebutton';
import { ref, computed, onMounted, watch } from 'vue';

const emit = defineEmits(['update:selectedChips']); // Declare the event


const props = defineProps({
    chipNames: {
        type: Array,
        required: true
    },
    selectedChipNames: {
        type: Array,
        required: true
    }
});

watch(
    () => props.selectedChipNames,
    (newVal, oldVal) => {
        // Your code here will run whenever `selectedChipNames` changes
        console.log(`ChipSelector.watch(selectedChipNames) Selected chips: props.selectedChipNames=${props.selectedChipNames}`)
        selectedChips.value = props.selectedChipNames;
    }
);

const selectedChips = ref([]); // Array to track selected chips
const chipEntries = computed(() => {
    console.log(`ChipSelector.computed() selectedChips.value=${selectedChips.value}, props.chipNames=${props.chipNames}`);
    return props.chipNames.map(name => ({ name, selected: selectedChips.value.includes(name) }))
});

onMounted(() => {
    console.log(`ChipSelector.onMounte() Selected chips: props.selectedChipNames=${props.selectedChipNames}`)
    selectedChips.value = props.selectedChipNames;
});

const toggleChipSelection = (name) => {
    if (selectedChips.value.includes(name)) {
        selectedChips.value = selectedChips.value.filter(chip => chip !== name);
    } else {
        selectedChips.value = [...selectedChips.value, name];
    }
    console.log("Selected chips: ", selectedChips.value);
    emit('update:selectedChips', selectedChips.value);
};

// Emit the list of selected chips back to the parent component
emit('update:selectedChips', selectedChips.value);  
</script>

