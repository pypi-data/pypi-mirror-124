import * as React from 'react';
import Spawner from '../Spawner';
import { shallow } from 'enzyme';

describe('Spawner test', () => {
  it('should render a basic component', () => {
    const component = shallow(<Spawner />);
    expect(component.html()).toMatchSnapshot('basic');
  });
});
