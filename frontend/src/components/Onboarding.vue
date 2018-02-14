<template>
  <div class="container">
    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex md3>
          <v-list class="accent">
            <v-list-tile to="/info/what-is-it">
              <v-list-content class="subheading black--text" >
                Was ist Gerrymandering?
              </v-list-content>
            </v-list-tile>
            <v-divider />
            <v-divider />
            <v-list-tile to="/info/make-use-of-it">
              <v-list-content class="subheading black--text" >
                Was kann man damit machen?
              </v-list-content>
            </v-list-tile>
          </v-list>
        </v-flex>
        <v-flex md6>
          <div class="white orange--text" v-if="$route.params.slug === 'what-is-it'">
            <v-toolbar class="black white--text">
              <v-btn icon to="/info">
                <v-icon>close</v-icon>
              </v-btn>
              <v-toolbar-title>
                Was ist Gerrymandering
            </v-toolbar-title>
            </v-toolbar>
            <div class="info-text subheading">
            <p>
              In einem Wahlsystem, in dem Sitze/Ämter an denjenigen vergeben werden,
              der die meisten Stimmen auf sich vereinigen kann, macht Gerrymandering Sinn.
              Da es völlig unerheblich ist, ob man einen Wahlbezirk mit 60% oder 80%
              der Stimmen, kann das Neu-Zeichnen der Bezirksgrenzen zu anderen Wahlergebnissen führen.
            </p>
            <p>
              Der Begriff Gerrymandering stammt aus den USA.
              Als erstmals Politker Wahlbezirke nach ihren Vorstellungen formten,
              kommentierte wurde ein Bezirk mit dem Kommentar bedacht "It looks like a gerrymander".
            </p>
            </div>
          </div>
          <div class="white orange--text" v-if="$route.params.slug === 'make-use-of-it'" >
            <v-toolbar class="black white--text">
              <v-btn icon to="/info">
                <v-icon>close</v-icon>
              </v-btn>
              <v-toolbar-title>
                Was kann man damit machen
            </v-toolbar-title>
            </v-toolbar>
            <div class="info-text subheading">
            <p class="title">
              Es gibt grundsätzlich zwei Strategien, wie man Wahlbezirke zu seinem
              Vorteil verändern kann:
            </p>
            <ol>
              <li>So viele Bereiche, in denen Anhänger des politischen Rivalen in einem einzigen Wahlbezirk
                zusammen fassen. Auf diese Weise erhält der Gegner so wenig Bezirke wie möglich.
              </li>
              <li>
                Bereiche, die man kontrolliert werden um kleine Bereiche erweitert, die dem Gegner gehören.
                Es darf aber nur so viel hinzu gefügt werden, dass man trotzdem noch die Mehrheit in seiner politischen Heimat hält.
              </li>
            </ol>
            </div>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
  export default {
    name: 'onboarding'
  }
</script>

<style lang="sass" scoped>
.container
  display: block
.info-text
  padding: 2em
</style>
