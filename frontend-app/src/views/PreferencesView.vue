<template>
  <div class="preferences-view">
    <div class="preferences-header">
      <div class="preferences-info">
        <h1>Match Preferences</h1>
        <p>Choose the traits, hobbies and lifestyle of the people you're looking to connect with!</p>
      </div>
      <div class="preferences-save-button">
        <n-button class="icon-btn" :style="{ backgroundColor: '#58CCD0' }" @click="savePreferences">
          <span>Save Changes</span>
        </n-button>
      </div>
    </div>
    <div class="preferences-container">
      <div class="preference-field slider-field">
        <span>Age</span>
        <n-space vertical>
          <n-slider 
          v-model:value="age_range" 
          range :step="1" 
          :min="18" :max="89" 
          :marks="age_marks"
          :show-tooltip="true"/>
        </n-space>
      </div>
      <div class="preference-field binary-choice-field">
        <span>Gender</span>
        <n-space vertical>
          <n-radio-group 
          v-model:value="gender" 
          name="radiobuttongroup1">
            <n-radio-button
              v-for="gender in genders"
              :key="gender.value"
              :value="gender.value"
              :label="gender.label"
            />
          </n-radio-group>
        </n-space>
      </div>
      <div class="preference-field multiplie-choice-field">
        <span>Filter by your hobbies</span>
        <n-space vertical>
          <n-select v-model:value="filtered_hobbies" 
          multiple :options="hobbies" />
        </n-space>
      </div>
      <div class="preference-field dropdown-field">
        <span>Lifestyle</span>
        <n-space vertical>
          <n-select v-model:value="lifestyle" 
          :options="lifestyles"
          placeholder="What is their lifestyle?"/>
        </n-space>
      </div>
      <div class="preference-field dropdown-field">
       <span>Dating Goals</span>
       <n-space vertical>
          <n-select v-model:value="dating_goal" 
          :options="dating_goals"
          placeholder="What are they looking for?"/>
        </n-space>
      </div>
      <div class="preference-field slider-field">
        <span>Distance</span>
        <n-space vertical>
          <n-slider v-model:value="distance" 
          :step="1" :min="2" :max="160" :marks="distance_marks"
          :show-tooltip="true"/>
        </n-space>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { NButton, NSlider, NSpace, NRadioGroup, NRadioButton, NSelect } from 'naive-ui'
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axios'

export default defineComponent({
  components: {
    NButton, NSlider, NSpace, NRadioButton, NRadioGroup, NSelect
  },
  setup() {
    const router = useRouter()
    
    // Zmienne reaktywne — puste lub null na start
    const age_range = ref([25, 35])
    const age_min = 18
    const age_max = 89
    const age_marks = { 18: '18', 89: '89' }

    const gender = ref(null)
    const genders = ref([
      { value: 'K', label: 'Female' },
      { value: 'M', label: 'Male' }
    ])

    const filtered_hobbies = ref([])
    const hobbies = ref([])

    const distance = ref(30)
    const distance_marks = { 2: '2', 160: '160' }

    const lifestyle = ref(null)
    const lifestyles = ref([])

    const dating_goal = ref(null)
    const dating_goals = ref([])

    async function savePreferences() {
      try {
        const payload = {
          preferred_gender: gender.value,
          age_min: age_range.value[0],
          age_max: age_range.value[1],
          preferred_distance: distance.value,
          preferred_lifestyle: lifestyle.value,
          preferred_goal: dating_goal.value,
          preferred_hobbies: filtered_hobbies.value,
        }
        await axios.post('/preferences/set/', payload)
        alert('Preferencje zapisane pomyślnie!')
        // Opcjonalnie: przekieruj na inną stronę, np. home
        router.push('/')
      } catch (err) {
        alert('Błąd podczas zapisywania preferencji')
        console.error(err)
      }
    }

    onMounted(async () => {
      try {
        const [lifestylesRes, goalsRes, traitsRes] = await Promise.all([
          axios.get('/lifestyles/'),
          axios.get('/relationship-goals/'),
          axios.get('/traits/')
        ])

        lifestyles.value = lifestylesRes.data.map((item: any) => ({
          label: item.name,
          value: item.id.toString()
        }))

        dating_goals.value = goalsRes.data.map((item: any) => ({
          label: item.name,
          value: item.id.toString()
        }))

        hobbies.value = traitsRes.data.map((item: any) => ({
          label: item.name,
          value: item.id.toString()
        }))

        // lifestyle.value = lifestyles.value[0]?.value || null
        // dating_goal.value = dating_goals.value[0]?.value || null
        // filtered_hobbies.value = hobbies.value.length > 0 ? [hobbies.value[0].value] : []

        const prefs = await axios.get('/preferences/')
        age_range.value = [prefs.data.age_min, prefs.data.age_max]
        gender.value = prefs.data.preferred_gender?.toUpperCase() || null
        lifestyle.value = prefs.data.preferred_lifestyle?.id.toString() || null
        dating_goal.value = prefs.data.preferred_goal?.id.toString() || null
        filtered_hobbies.value = prefs.data.preferred_hobbies.map((h: any) => h.id.toString())
        distance.value = prefs.data.preferred_distance || 30

      } catch (e) {
        console.error('Failed to load preferences data', e)
      }
    })
    
    return {
      age_range,
      age_min,
      age_max,
      age_marks,
      gender,
      genders,
      filtered_hobbies,
      hobbies,
      distance,
      distance_marks,
      lifestyle,
      lifestyles,
      dating_goal,
      dating_goals,
      savePreferences
    }
  }
})

</script>

<style scoped>
.preferences-view {
  background-color: #FFC4C4;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  height: 100%;
  border-radius: 10px;
}

.preferences-header {
  display: flex;
  justify-content: space-between;
  width: 95%;
  align-items: center;
}

.preferences-info {
  max-width: 25%;
}

.preferences-save-button {
  border-radius: 10px;
}

.icon-btn {
  border-radius: 15px;
  padding: 30px;
}

.preferences-save-button span {
  font-size: 30px;
  padding: 10px;
}

.preferences-container {
  background-color: #FFDCDC;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  height: 100%;
  width: 95%;
  border-radius: 10px;
}

.preference-field {
  background-color: #FFFFFF;
  margin: 10px;
  border-radius:10px;
  padding: 10px;
}

.preference-field span {
  font-weight: bold;
}

.slider-field {
  max-width: 100%;
}

.binary-choice-field {
  max-width: 25%;
}

.multiple-choice-field {
  max-width: 75%;
}

.dropdown-field {
  max-width: 25%;
}
</style>