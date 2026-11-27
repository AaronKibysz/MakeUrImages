import { StyleSheet, Text, View } from "react-native";

// Placeholder para el flujo de creacion (T-045+).
// Esta pantalla se implementara en tareas posteriores.

export default function CreateScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crear publicacion</Text>
      <Text style={styles.subtitle}>Pantalla en construccion</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
  },
  subtitle: {
    marginTop: 8,
    fontSize: 14,
    color: "#666",
  },
});