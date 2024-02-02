import { Image, Text } from "react-native";
import { Container, Header } from "./styles";
import LOGO_IMAGE from '@assets/logo.jpg'
import PROFILE_IMAGE from '@assets/profile.jpg'
import { PercentageCard } from "@components/PercentageCard";

export function Home() {
    return (
        <Container>
            <Header>
                <Image source={LOGO_IMAGE} style={{ width: 82, height: 37}}/>
                <Image source={PROFILE_IMAGE} style={{ width: 40, height: 40}}/>
            </Header>
            <PercentageCard />
        </Container>
    )
}