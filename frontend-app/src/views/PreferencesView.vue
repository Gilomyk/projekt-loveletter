<template>
  <div class="preferences-view">
    <div class="preferences-header">
      <div class="preferences-info">
        <h1>Match Preferences</h1>
        <p>Choose the traits, hobbies and lifestyle of the people you're looking to connect with!</p>
      </div>
      <div class="preferences-save-button">
        <n-button class="icon-btn" :style="{ backgroundColor: '#58CCD0' }">
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
import { defineComponent, ref } from 'vue'

export default defineComponent({
  components: {
    NButton, NSlider, NSpace, NRadioButton, NRadioGroup, NSelect
  },
  setup() {
    return {
      age_range: ref([25, 35]),
      age_min: 18,
      age_max: 89,
      age_marks: {
        18: '18',
        89: '89'
      },
      gender: ref(null),
      genders: [
        {
          value: 'Male',
          label: 'Male'
        },
        {
          value: 'Female',
          label: 'Female'
        }
      ].map((s) => {
        s.value = s.value.toLowerCase()
        return s
      }),
      filtered_hobbies: ref(['hobby0']),
      hobbies: [
        {
          label: 'Climbing',
          value: 'hobby0'
        },
        {
          label: 'Fencing',
          value: 'hobby1'
        },
        {
          label: 'Computer Games',
          value: 'hobby2'
        },
        {
          label: 'Coding',
          value: 'hobby3'
        },
        {
          label: 'Hiking',
          value: 'hobby4'
        },
      ],
      distance: ref(30),
      distance_marks: {
        2: '2',
        160: '160'
      },
      lifestyle: ref(null),
      lifestyles: [
        {
          label: 'Party Animal',
          value: 'lifestyle0'
        },
        {
          label: 'Homebody',
          value: 'lifestyle1'
        },
        {
          label: 'Married to the Grind',
          value: 'lifestyle2'
        },
        {
          label: 'Academic Weapon',
          value: 'lifestyle3'
        },
        {
          label: 'Wilderness Explorer',
          value: 'lifestyle4'
        }
      ],
      dating_goal: ref(null),
      dating_goals: [
        {
          label: 'Still thinking about it',
          value: 'dating_goal0'
        },
        {
          label: 'Long-term relationship',
          value: 'dating_goal1'
        },
        {
          label: 'Short-term fun',
          value: 'dating_goal2'
        },
        {
          label: 'Marriage',
          value: 'dating_goal3'
        }
      ]
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
  max-width: 15%;
}

.preferences-save-button {
  border-radius: 10px;
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