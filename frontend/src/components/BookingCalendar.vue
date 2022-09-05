<template>
  <div class="container text-center">
    <h1>Choose your interval</h1>
    <vue-meeting-selector
      ref="meetingSelector"
      class="meeting-selector"
      v-model="meeting"
      :date="date"
      :loading="false"
      :meetings-days="meetingsDays"
      @next-date="nextDate"
      @previous-date="previousDate"
    >
    </vue-meeting-selector>
    <p>meeting Selected: {{ meeting ? meeting : "No Meeting selected" }}</p>
    <button @click="submit" class="btn btn-primary">Book interval</button>
    {{ bookedIntervals }}
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import VueMeetingSelector from "vue-meeting-selector";
import slotsGenerator from "vue-meeting-selector/src/helpers/slotsGenerator";
import api from "@/api.js";

export default defineComponent({
  data () {
    return {
      bookedIntervals: window.hydrate.booked_intervals
    }
  },
  components: {
    VueMeetingSelector,
  },
  setup() {
    const meeting = ref(null);
    const meetingsDays = ref([]);
    const nbDaysToDisplay = ref(5);
    const date = ref(new Date());

    const initMeetingsDays = () => {
      const start = {
        hours: 0,
        minutes: 0,
      };
      const end = {
        hours: 23,
        minutes: 0,
      };
      meetingsDays.value = slotsGenerator(
        new Date(),
        nbDaysToDisplay.value,
        start,
        end,
        60
      );
    };

    initMeetingsDays();

    const meetingSelector = ref(null);

    const up = () => meetingSelector.value.previousMeetings();

    const down = () => meetingSelector.value.nextMeetings();

    const nextDate = () => {
      const start = {
        hours: 8,
        minutes: 0,
      };
      const end = {
        hours: 16,
        minutes: 0,
      };
      const d = new Date(date.value);
      const newDate = new Date(d.setDate(d.getDate() + 7));
      date.value = newDate;
      meetingsDays.value = slotsGenerator(
        newDate,
        nbDaysToDisplay.value,
        start,
        end,
        30
      );
    };

    const previousDate = () => {
      const start = {
        hours: 8,
        minutes: 0,
      };
      const end = {
        hours: 16,
        minutes: 0,
      };
      const d = new Date(date.value);
      d.setDate(d.getDate() - 7);
      const formatingDate = (dateToFormat) => {
        const dateParsed = new Date(dateToFormat);
        const day =
          dateParsed.getDate() < 10
            ? `0${dateParsed.getDate()}`
            : dateParsed.getDate();
        const month =
          dateParsed.getMonth() + 1 < 10
            ? `0${dateParsed.getMonth() + 1}`
            : dateParsed.getMonth() + 1;
        const year = dateParsed.getFullYear();
        return `${year}-${month}-${day}`;
      };
      const newDate =
        formatingDate(new Date()) >= formatingDate(d)
          ? new Date()
          : new Date(d);
      date.value = newDate;
      meetingsDays.value = slotsGenerator(
        newDate,
        nbDaysToDisplay.value,
        start,
        end,
        30
      );
    };

    return {
      meeting,
      meetingsDays,
      date,
      meetingSelector,
      up,
      down,
      nextDate,
      previousDate,
    };
  },
  methods: {
    async submit() {
      try {
        await api.saveForm("", this.meeting)
      } catch (e) {
        alert("The interval is already taken. Choose another interval and try again.");
      }
    }
  }
});
</script>

<style scoped>
  .meeting-selector {
    padding: 100px;
  }
</style>