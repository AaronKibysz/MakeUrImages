import { StyleSheet, Text, View } from "react-native";

// Placeholder para el editor limitado (T-048+).

export default function EditorScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Editor</Text>
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