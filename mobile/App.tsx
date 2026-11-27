import { StatusBar } from "expo-status-bar";
import { View } from "react-native";

import CreateScreen from "./src/screens/create/CreateScreen";

export default function App() {
  return (
    <View style={{ flex: 1 }}>
      <CreateScreen />
      <StatusBar style="auto" />
    </View>
  );
}