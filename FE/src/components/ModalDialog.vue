<template>
    <Dialog :visible="visible" :modal="true" :closable="false">
        <template #header>
            <h2>{{ title }}</h2>
        </template>
        <p>{{ message }}</p>
        <template #footer>
            <Button label="Close" @click="close" />
        </template>
    </Dialog>
</template>

<script setup>
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';

const props = defineProps({
    title: {
        type: String,
        required: true,
    },
    message: {
        type: String,
        required: true,
    },
    visible: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(['update:visible']);

const close = () => {
    console.log('close');
    emit('update:visible', false);
};
</script>
