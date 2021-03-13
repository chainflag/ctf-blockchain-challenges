<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="rwctf"
          class="shrink hidden-sm-and-down"
          contain
          :src="require('./assets/logo.png')"
          width="200"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn text @click="flagDialog = true">
        <span class="mr-2">Get The Flag</span>
        <v-icon>mdi-flag-minus-outline</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <Billboard />
      <v-snackbar v-model="msgVisible">
        {{ message }}

        <template v-slot:action="{ attrs }">
          <v-btn color="blue" text v-bind="attrs" @click="msgVisible = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>

    <v-dialog v-model="flagDialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Get The Flag</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form ref="form" lazy-validation>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="flagForm.token"
                    label="Token"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="flagForm.txHash"
                    label="TxHash"
                    :rules="[rules.required, rules.length]"
                    counter
                    maxlength="64"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="flagDialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text @click="handleSubmit">
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from "axios";
import md5 from "crypto-js/md5";

import Billboard from "./components/Billboard";

export default {
  name: "App",

  components: {
    Billboard
  },

  data: () => ({
    flagDialog: false,
    msgVisible: false,
    message: "",
    flagForm: {
      token: "",
      txHash: ""
    },
    rules: {
      required: value => !!value || "Required.",
      length: value => (value && value.length === 64) || "Invalid length."
    }
  }),
  methods: {
    handleSubmit() {
      if (!this.$refs.form.validate()) {
        return;
      }
      axios
        .get("/api/v1/flag", {
          params: {
            token: md5(this.flagForm.token).toString(),
            tx: this.flagForm.txHash
          }
        })
        .then(res => {
          if (res.data.err === "") {
            console.log(res.data);
            this.handleMessageBox(res.data.data);
          } else {
            this.handleMessageBox(res.data.err);
          }
        })
        .catch(error => {
          this.handleMessageBox(error.response.status);
        });
    },
    handleMessageBox(message) {
      this.message = message;
      this.msgVisible = true;
    }
  }
};
</script>
