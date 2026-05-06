import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  name: "",
  date: "",
  time: "",
  attendees: "",
  topics: "",
  materials: "",
  samples: "",
  sentiment: "",
  outcomes: "",
  followup: "",
};

const formSlice = createSlice({
  name: "form",
  initialState,

  reducers: {
    updateForm: (state, action) => {
      return {
        ...state,
        ...action.payload,
      };
    },

    resetForm: () => initialState,
  },
});

export const { updateForm, resetForm } = formSlice.actions;

export default formSlice.reducer;
