<template>
    <div class="container">
        <div class="header">
            <h1>Reports</h1>
        </div>
        <div class="no-reports-container" v-if="!reports.length">
            <div class="no-report-information">
                <h1>No reports!</h1>
                <p>There are no reports to handle. Wait for user reports.</p>
            </div>
        </div>
        <div class="reports-container" v-else>
            <ul>
                <li 
                    v-for="(report) in reports"
                    :key="report.id"
                >
                    <div class="report">
                        <div class="report-title">
                            <h4>Report</h4>
                        </div>
                        <div class="report-users">
                            <span>Reporter: {{ report.reporter.first_name }}</span>
                            <span>Reported: {{ report.reported.first_name }}</span>
                        </div>
                        <div class="report-content">
                            <span>Reasoning:</span>
                            <p>{{ report.reasoning }}</p>
                        </div>
                    </div>
                    <div class="report-actions">
                        <n-button class="btn" :style="{ backgroundColor: '#ef4444' }" @click="denyReport(report)">
                            <p>Deny</p>
                        </n-button>
                        <n-button class="btn" :style="{ backgroundColor: '#44EF44' }" @click="acceptReport(report)">
                            <p>Accept</p>
                        </n-button>                        
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import axios from "@/axios";
import { NIcon, NButton } from "naive-ui";
import { Phone, Hammer } from "@vicons/fa";
import { Send16Regular } from "@vicons/fluent";
import { useRouter } from 'vue-router';

interface User {
    id: number
    first_name: string
    age: number
    profile_picture: string
}

interface Report {
    id: number
    reporter: User
    reported: User
    reasoning: string
}

export default defineComponent({
  name: "ChatView",
  components: {
    NIcon,
    NButton,
    Phone,
    Send16Regular,
    Hammer
  },
  data() {
    return {
      currentUserId: 0,
      allReports: [],
      reports: [
        {
            id: 1,
            reporter: {id: 0, first_name: 'jan', age: 24, profile_picture: 'alt-picture'},
            reported: {id: 1, first_name: 'jonasz', age: 24, profile_picture: 'alt-picture'},
            reasoning: 'Bo byl strasznie niemily'
        },{
            id: 2,
            reporter: {id: 0, first_name: 'jan', age: 24, profile_picture: 'alt-picture'},
            reported: {id: 1, first_name: 'jonasz', age: 24, profile_picture: 'alt-picture'},
            reasoning: 'Bo byl strasznie niemily'
        },{
            id: 3,
            reporter: {id: 0, first_name: 'jan', age: 24, profile_picture: 'alt-picture'},
            reported: {id: 1, first_name: 'jonasz', age: 24, profile_picture: 'alt-picture'},
            reasoning: 'Bo byl strasznie niemily'
        }
      ],
      router: useRouter(),
    };
  },
  computed: {

  },
  methods: {
    fetchReports() {
    axios.get('/reports/')
      .then((response) => {
        this.reports = response.data;
      })
      .catch((error) => {
        console.error('Błąd podczas pobierania zgłoszeń:', error);
      });
  },
    denyReport(report) {
      axios.post(`/report/${report.id}/deny/`)
        .then(() => {
          const index = this.reports.indexOf(report);
          if (index > -1) this.reports.splice(index, 1);
        })
        .catch((error) => {
          console.error('Błąd przy odrzuceniu zgłoszenia:', error);
        });
    }
,
    acceptReport(report) {
      axios.post(`/report/${report.id}/accept/`)
        .then(() => {
          const index = this.reports.indexOf(report);
          if (index > -1) this.reports.splice(index, 1);
        })
        .catch((error) => {
          console.error('Błąd przy akceptacji zgłoszenia:', error);
        });
    }
  },
  mounted() {
  this.fetchReports();
}

});
</script>

<style scoped>
.container {
    background-color: #FFCBCB;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px;
    height: 82vh;
    border-radius: 10px;
}

.header {
  height: auto;
  width: 95%;
  flex-shrink: 0;
  margin-left: 10px;
}

.no-reports-container {
  padding-top: 10%;
  padding-bottom: 10%;
  background-color: #FFDFDF;
  height: 100%;
  width: 95%;
  border-radius: 10px;
  margin: 1vh;
  text-align: center;
  align-items: center;
  font-size: 20px;
}

.reports-container {
  background-color: #FFDFDF;
  max-height: 100%;
  width: 95%;
  height: 100%;
  margin-bottom: 1vh;
  border-radius: 10px;
  text-align: center;
  font-size: 20px;
  overflow-y: scroll;
}

ul {
    list-style: none;
    display: flex;
    flex-direction: column;
}

li {
    display: flex;
    flex-direction: column;
    background-color: #fffdfd;
    border-radius: 10px;
    font-size: 20px;
    margin-bottom: 1%;
    margin-right: 3%;
}

.report {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: start end;
    margin-left: 1%;
}

.report-users {
    display: flex;
    flex-direction: column;
    align-items: start;
}

.report-content {
    display: flex;
    flex-direction: column;
    align-items: start;
    width: 95%;
}

.report-content p {
    border-radius: 10px;
    background-color: #e79494;
    text-align: start;
    padding: 2%;
    max-width: 100%;
}

.report-actions {
    display: flex;
    flex-direction: row;
    justify-content: end;
    gap: 15px;
    margin-right: 1%;
    margin-bottom: 1%;
}

.btn {
    border-radius: 8px;
    padding: 2%;
}

.btn p {
    font-size: 20px;
    font-weight: bolder;
    padding: 5%;
}

</style>