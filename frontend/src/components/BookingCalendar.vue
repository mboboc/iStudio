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
     <template #meeting="{ meeting }">
        <div
          v-if="meeting.date"
          :class="meetingSelectedClass(meeting)"
          @click="selectMeeting(meeting)">
          {{ formatingTime(meeting.date) }}
        </div>
        <div v-else class="meeting--empty">
          &mdash;
        </div>
      </template>
    </vue-meeting-selector>
    <h2>{{ meeting ? `${getDayOfTheWeek(meeting.date)}, ${meeting.date.getUTCDate()} ${getMonth(meeting.date)} at ${formatingTime(meeting.date)}, ${getTimeZone()} time` : "No interval selected" }}</h2>
    <button v-if="meeting" @click="submit" class="btn btn-dark btn-lg">Book interval</button>
    <button v-else class="btn btn-dark btn-lg" disabled>Book interval</button>

  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import VueMeetingSelector from "vue-meeting-selector";
import slotsGenerator from "vue-meeting-selector/src/helpers/slotsGenerator";
import api from "@/api.js";

var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];

export default defineComponent({
  data () {
    return {
      bookedIntervals: window.hydrate.booked_intervals
    }
  },
  computed: {
    bookedIntervalsTime() {
      return this.bookedIntervals.map(date => new Date(date).getTime())
    }
  },
  components: {
    VueMeetingSelector,
  },
  setup() {
    const meeting = ref(null);
    const meetingsDays = ref([]);
    const nbDaysToDisplay = ref(7);
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
        hours: 0,
        minutes: 0,
      };
      const end = {
        hours: 23,
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
        60
      );
    };

    const previousDate = () => {
      const start = {
        hours: 0,
        minutes: 0,
      };
      const end = {
        hours: 23,
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
        60
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
        await api.saveForm("", this.meeting).then(function(response) {
          return response.json();
        }).then(function(data) {
          window.location.href = `qr/${data.date}`
        });
      } catch (e) {
        alert("The interval is already taken. Choose another interval and try again.");
      }
    },
    // display meeting selected diferently
    meetingSelectedClass(meeting) {
      const booked = this.bookedIntervalsTime?.includes(this.getDateFormat(meeting))
      if (booked)
        return 'meeting meeting--readonly'
      if (!this.meeting) {
        return booked ? 'meeting--readonly' : 'meeting'
      }
      const selectedDate = new Date(meeting.date);
      const date = new Date(this.meeting.date);
      if (selectedDate.getTime() === date.getTime()) {
        return 'meeting meeting--selected';
      }
      return this.bookedIntervalsTime?.includes(this.getDateFormat(meeting)) ? 'meeting--readonly' : 'meeting'
    },
    // @click on meeting
    selectMeeting(meeting) {
      if (this.meeting) {
        const selectedDate = new Date(meeting.date);
        const date = new Date(this.meeting.date);
        if (selectedDate.getTime() !== date.getTime()) {
          this.meeting = meeting;
        } else {
          this.meeting = undefined;
        }
      } else {
        this.meeting = meeting;
      }
    },
    formatingDate(dateToFormat) {
      const d = new Date(dateToFormat);
      const day = d.getDate() < 10 ? `0${d.getDate()}` : d.getDate();
      const month = d.getMonth() + 1 < 10 ? `0${d.getMonth() + 1}` : d.getMonth() + 1;
      const year = d.getFullYear();
      return `${year}-${month}-${day}`;
    },
    formatingTime(date) {
      const d = new Date(date);
      const hours = d.getHours() < 10 ? `0${d.getHours()}` : d.getHours();
      const minutes = d.getMinutes() < 10 ? `0${d.getMinutes()}` : d.getMinutes();
      return `${hours}:${minutes}`;
    },
    getDateFormat(meeting) {
      if (!meeting)
        return ""
      return new Date(meeting.date).getTime();
    },
    getDayOfTheWeek(date) {
      return days[date.getDay()];
    },
    getMonth(date) {
      return months[date.getMonth()];
    },
    getTimeZone() {
      return Intl.DateTimeFormat().resolvedOptions().timeZone
    }
  }
});
</script>

<style scoped lang="scss">
.meeting-selector {
    padding: 20px;
  }
.slots-example {
  &__meeting-selector {
    max-width: 542px;
  }
}
.title {
  margin: 0 5px;
}
.meeting {
  display: inline-block;
  padding: 50px;
  margin: 5px 0;
  background-color: #23E795;
  border-radius: 4px;
  color: black;
  cursor: pointer;
  &--selected {
    background-color: #B39CD0;
  }
  &--empty {
    display: inline-block;
    padding: 5px;
    margin: 5px 0;
    cursor: not-allowed;
  }
  &--readonly {
    background-color: #DD2D4A;
    cursor: not-allowed;
    display: inline-block;
  }
}
.button-pagination {
  border: none;
  padding: 0;
  width: 30px;
}
// since our scss is scoped we need to use ::v-deep
::v-deep .loading-div {
  top: 32px!important;
}
</style>