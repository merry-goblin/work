const app = Vue.createApp({
  data() {
    return {
      enteredTaskValue: '',
      taskList: [],
      toggleLabel: 'Hide list'
    };
  },
  computed: {
    hideOrShowTaskList() {
      return (this.toggleLabel !== 'Show list');
    }
  },
  methods: {
    addTask() {
      this.taskList.push(this.enteredTaskValue);
    },
    toggleList() {
      this.toggleLabel = (this.toggleLabel === 'Hide list') ? 'Show list' : 'Hide list';
    }
  }
});

app.mount('#assignment');