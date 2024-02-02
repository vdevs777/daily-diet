import { ArrowUpRight } from "phosphor-react-native";
import styled from "styled-components/native";

export type PercentageCardTypeStyleProps = 'POSITIVE' | 'NEGATIVE';

type Props = {
    type: PercentageCardTypeStyleProps
}

export const Container = styled.View<Props>`
  width: 100%;
  height: 102px;
  background-color: ${({ theme, type }) => type === 'POSITIVE' ?  theme.COLORS.GREEN_LIGHT : theme.COLORS.RED_LIGHT};
  border-radius: 7px;
  padding: 8px;
`;

export const Icon = styled(ArrowUpRight)<Props>`
  color: ${({ theme, type }) => type === 'POSITIVE' ?  theme.COLORS.GREEN_DARK : theme.COLORS.RED_DARK};
`;

export const IconContainer = styled.View`
  align-items: flex-end;
`;

export const TextContainer = styled.View`
  align-items: center;
  justify-content: center;
`

export const Percentage = styled.Text`
  font-size: ${({theme}) => theme.FONT_SIZE.XXL}px;
  font-family: ${({ theme }) => theme.FONT_FAMILY.REGULAR}
`