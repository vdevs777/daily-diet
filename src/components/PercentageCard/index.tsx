import { Text } from "react-native";
import { Container, Icon, IconContainer, Percentage, TextContainer } from "./styles";
import { ArrowUpRight } from "phosphor-react-native";

export function PercentageCard() {
    return (
        <Container type="POSITIVE">
            <IconContainer>
                <Icon type="POSITIVE" />
            </IconContainer>
            <TextContainer>
                <Percentage>90,86%</Percentage>
            </TextContainer>
        </Container>
    )
}