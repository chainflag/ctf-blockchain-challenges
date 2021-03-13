<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="result"
      :items-per-page="15"
      :search="search"
      disable-sort
    ></v-data-table>
  </v-card>
</template>
<script>
import axios from "axios";

export default {
  data: () => ({
    search: "",
    headers: [
      {
        text: "Creator",
        align: "start",
        value: "creator"
      },
      { text: "Content", value: "content" },
      {
        text: "Deposit",
        filterable: false,
        value: "deposit"
      }
    ],
    result: []
  }),
  created() {
    this.fetchAdvertisements();
  },

  methods: {
    fetchAdvertisements() {
      axios
        .get("/billboard/advertisement")
        .then(res => {
          console.log(res);
          for (let element of res.data.result) {
            let advertisement = {
              creator: element.creator,
              content: element.content,
              deposit: element.deposit.amount
            };
            this.result.push(advertisement);
          }
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>
